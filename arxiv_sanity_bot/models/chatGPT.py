from arxiv_sanity_bot.events import RetryableErrorEvent, FatalErrorEvent
from arxiv_sanity_bot.models.model import LLM
from arxiv_sanity_bot.config import CHATGPT_N_TRIALS, MESSAGE_TEXT_LENGTH
import time
import openai


class ChatGPT(LLM):
    def summarize_abstract(self, abstract: str) -> str:

        summary = ""

        for i in range(CHATGPT_N_TRIALS):
            history = [
                {
                    "role": "system",
                    "content": f"You are a discord chat bot. You can only answer with a maximum of "
                               f"{MESSAGE_TEXT_LENGTH-300} characters. Answers should be casual and "
                               f"engaging. They should easy to read and may include Discord's markup: "
                               f"use *word* for cursive and **word** for bold text.",
                },
                {
                    "role": "user",
                    "content": f"Summarize the following abstract in a few short sentence: `{abstract}`. ",
                },
            ]

            r = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0301",
                messages=history,
            )
            time.sleep(45)

            summary = r["choices"][0]["message"]["content"].strip()

            if len(summary) <= MESSAGE_TEXT_LENGTH:
                # This is a good tweet
                break
            else:
                RetryableErrorEvent(
                    msg=f"Summary was {len(summary)} characters long instead of {MESSAGE_TEXT_LENGTH}.",
                    context={
                        "abstract": abstract,
                        "this_summary": summary
                    }
                )
        else:

            FatalErrorEvent(
                msg=f"ChatGPT could not successfully generate a tweet after {CHATGPT_N_TRIALS}",
                context={
                    "abstract": abstract
                }
            )

        return summary
