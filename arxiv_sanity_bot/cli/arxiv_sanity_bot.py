import os
from datetime import datetime, timedelta
import time
import asyncio
import random

import pandas as pd
import pyshorteners
import requests.exceptions

from arxiv_sanity_bot.arxiv_sanity.abstracts import get_all_abstracts
from arxiv_sanity_bot.config import (
    PAPERS_TO_SUMMARIZE,
    WINDOW_START,
    WINDOW_STOP,
    TIMEZONE,
    SHORTEN_URL,
    ABSTRACT_CACHE_FILE,
    INTRO_LINES,
    OUTRO_LINES,
)
from arxiv_sanity_bot.events import InfoEvent, RetryableErrorEvent
from arxiv_sanity_bot.models.chatGPT import ChatGPT
from arxiv_sanity_bot.twitter.auth import TwitterOAuth1
from arxiv_sanity_bot.twitter.send_tweet import send_tweet
from arxiv_sanity_bot.discord.connection import DiscordConnection


def bot():

    InfoEvent(msg="Bot starting")

    abstracts, start, end = _gather_abstracts()

    if abstracts.shape[0] == 0:

        InfoEvent(msg=f"No abstract in the time window {start} - {end}")

    # Summarize the top 10 papers
    summaries = _summarize_top_abstracts(abstracts, n=PAPERS_TO_SUMMARIZE)

    discord_connection = DiscordConnection()

    @discord_connection.client.event
    async def on_ready():
        for s in summaries:
            await discord_connection.send(s)
            time.sleep(1)
        await discord_connection.close()

    discord_connection.run()

    InfoEvent(msg="Bot finishing")


def _summarize_top_abstracts(abstracts, n):

    # This is indexed by arxiv number
    already_processed_df = (
        pd.read_parquet(ABSTRACT_CACHE_FILE)
        if os.path.exists(ABSTRACT_CACHE_FILE)
        else None
    )

    summaries = []
    processed = []
    for i, row in abstracts.iloc[:n].iterrows():

        summary, short_url = _summarize_if_new(already_processed_df, row)

        intro_line = random.choice(INTRO_LINES)
        outro_line = random.choice(OUTRO_LINES)

        if summary is not None:
            summaries.append(f"**{intro_line}**\n\n{summary}\n\n{outro_line} {short_url}")

            processed.append(row)

    _save_to_cache(already_processed_df, processed)

    return summaries


def _save_to_cache(already_processed_df, processed):
    if len(processed) > 0:

        processed_df = pd.DataFrame(processed).set_index("arxiv")

        if already_processed_df is not None:
            processed_df = pd.concat([already_processed_df, processed_df])

        processed_df.to_parquet(ABSTRACT_CACHE_FILE)


def _summarize_if_new(already_processed_df, row):

    chatGPT = ChatGPT()
    s = pyshorteners.Shortener()

    if already_processed_df is not None and row["arxiv"] in already_processed_df.index:
        # Yes, we already processed it. Skip it
        InfoEvent(
            f"Paper {row['arxiv']} was already processed in a previous run",
            context={"title": row["title"], "score": row["score"]},
        )
        summary, short_url = None, None
    else:
        summary = chatGPT.summarize_abstract(row["abstract"])

        url = f"https://arxiv-sanity-lite.com/?rank=pid&pid={row['arxiv']}"

        if not SHORTEN_URL:
            short_url = url
        else:
            for _ in range(10):
                # Remove the 'http://' part which is useless and consumes characters
                # for nothing
                try:
                    short_url = s.tinyurl.short(url).split("//")[-1]
                except requests.exceptions.Timeout as e:
                    RetryableErrorEvent(
                        msg="Could not shorten URL", context={"url": url, "error": str(e)}
                    )
                    time.sleep(10)
                    continue
                else:
                    break
            else:
                InfoEvent("Could not shorten URL. Dropping it from the tweet!")
                short_url = ""

    return summary, short_url


def _gather_abstracts():
    """
    Get all abstracts from arxiv-sanity from the last 48 hours

    :return: a pandas dataframe with the papers ordered by score (best at the top)
    """
    now = datetime.now(tz=TIMEZONE)
    abstracts = get_all_abstracts(
        after=now - timedelta(hours=WINDOW_START)
    )  # type: pd.DataFrame

    if abstracts.shape[0] == 0:
        return abstracts, now - timedelta(hours=WINDOW_START), now

    # Remove abstracts newer than 24 hours (as we need at least 24 hours to accumulate some
    # stats for altmetric)
    start = now - timedelta(hours=WINDOW_START)
    end = now - timedelta(hours=WINDOW_STOP)
    abstracts.query(
        "published_on.between(@start, @end)",
        inplace=True,
        local_dict={
            "start": start,
            "end": end,
        },
    )
    return abstracts, start, end


if __name__ == "__main__":

    bot()
