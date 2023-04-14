import os
import discord

from arxiv_sanity_bot.config import DISCORD_CHANNEL_ID, DSICORD_N_TRIALS, DISCORD_SLEEP_TIME
from arxiv_sanity_bot.events import InfoEvent, FatalErrorEvent, RetryableErrorEvent
from arxiv_sanity_bot.twitter.auth import TwitterOAuth1

class DiscordConnection:

    access_token: str = None
    client: discord.Client = None

    def __init__(self):
        self.access_token = os.environ.get("DISCORD_ACCESS_TOKEN", "")

        intents = discord.Intents.default()
        intents.guild_messages = True
        self.client = discord.Client(intents=intents)


    def run(self) -> None:
        self.client.run(self.access_token)

    async def close(self) -> None:
        await self.client.close()


    async def send(self, content: str) -> None:
        """
        Send a Discord Message.

        :param content: text to send. Must respect Discord's maximum length
        :param client: an instance of a discord.Client that's connected to their API
        """

        # Get the channel to send the message to
        channel = self.client.get_channel(DISCORD_CHANNEL_ID)

        if not channel:
            FatalErrorEvent(msg=f"Channel not found (ID = {DISCORD_CHANNEL_ID})")

        for i in range(DSICORD_N_TRIALS):
            try:
                await channel.send(content)

            except discord.Forbidden as e:
                FatalErrorEvent(
                    msg=f"Sending message forbidden.",
                    context={"exception": str(e), "content": content},
                )

            except discord.HTTPException as e:
                if (i + 1) < DSICORD_N_TRIALS:
                    RetryableErrorEvent(
                        msg=f"Could not send message. Retrying after {DISCORD_SLEEP_TIME} s",
                        context={"exception": str(e), "content": content},
                    )
                    time.sleep(DISCORD_SLEEP_TIME)
                    continue
                else:
                    FatalErrorEvent(
                        msg=f"Could not send message after {DSICORD_N_TRIALS}",
                        context={"exception": str(e), "content": content},
                    )

            else:
                break

        InfoEvent(msg=f"Sent message {content}")

        return