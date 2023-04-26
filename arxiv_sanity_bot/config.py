# Summarize the top N papers
from zoneinfo import ZoneInfo

PAPERS_TO_SUMMARIZE = 1

# This defines the time window to consider
WINDOW_START = 48  # hours ago
WINDOW_STOP = 24  # hours ago

# Number of times to try calling chatGPT before giving up
# (if chatGPT returns summaries that are too long)
CHATGPT_N_TRIALS = 10

SHORTEN_URL = False

# The url length depens on the url shortener used. For tinyurl is 18 if
# we remove https://
URL_LENGTH = 20
MESSAGE_TEXT_LENGTH = 500 - URL_LENGTH

# How many times to try to send a tweet before failing
TWITTER_N_TRIALS = 10
# Seconds to wait if sending a tweet fails, before retrying
TWITTER_SLEEP_TIME = 60

DISCORD_CHANNEL_ID = 1098138007401418765
DSICORD_N_TRIALS = 2
DISCORD_SLEEP_TIME = 1

# How many calls we can make in parallel for the Altmetric
# API
ALTMETRIC_CHUNK_SIZE = 10

# Characters allowed in an abstract
ABSTRACT_ALLOWED_CHARACTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,!?'- "

# Time to give to arxiv-sanity-lite to render the pages
# before trying to fetch them (in seconds)
ARXIV_SANITY_RENDERING_TIME = 5
# Max number of pages to fetch from arxiv-sanity in one go
ARXIV_SANITY_MAX_PAGES = 10
# How many pages to download concurrently from arxiv-sanity
ARXIV_SANITY_CONCURRENT_DOWNLOADS = 5
# How many times to retry in case of issues
ARXIV_SANITY_N_TRIALS = 10
# Seconds to wait if sending a download fails, before retrying
ARXIV_SANITY_SLEEP_TIME = 60
TIMEZONE = ZoneInfo("America/Los_Angeles")

ABSTRACT_CACHE_FILE = "posted_abstracts.parquet"

INTRO_LINES = [
    "Hey, you! Yes, you with the screen addiction. Check out this paper:",
    "Get ready to have your mind blown with this paper:",
    "Stop scrolling through memes and take a look at this research:",
    "I know you love data more than your ex. Check out this paper:",
    "You know what's cooler than winning a Fortnite match? This paper:",
    "Ready for some nerd talk? Here's a paper for you:",
    "Can't decide between Netflix and science? Here's a paper that's better than both:",
    "You won't believe what these scientists discovered in this paper:",
    "Don't let this paper be buried in your inbox. Check it out:",
    "No time for small talk. Here's a paper that will make you smarter:",
    "Buckle up, buttercup. This paper is about to take you on a wild ride:",
    "Forget about your latest TikTok obsession and check out this paper:",
    "Feeling a little dull today? This paper will spice things up:",
    "This paper is so fascinating, I bet you wish you had thought of it first.",
    "Don't be a couch potato, read this paper instead:",
    "You'll thank me later for recommending this paper:",
    "Can't find anything interesting to read? This paper will change that:",
    "Move over, Sherlock Holmes. This paper has all the clues:.",
    "Don't let your brain turn to mush. Read this paper:",
    "Feeling left behind? This paper will bring you up to speed:",
]

OUTRO_LINES = [
    "That's all for now. Until next time, here's the link to the paper I just shared:",
    "I'm off to find more interesting research, but don't forget to check out the paper I just posted:",
    "Time to say goodbye, but not before leaving you with the link to this thought-provoking paper:",
    "I'll be back with more exciting papers, but for now, don't miss out on this one:",
    "It's time for me to go, but before I do, make sure you read this paper:",
    "I'll be back with more great reads, but for now, here's the link to the paper I just summarized:",
    "My work here is done, but yours is just beginning. Check out this amazing paper:",
    "I'm out on the hunt for more papers to share, but don't forget to check out the one I just posted:",
    "That's it for now, but before I go, don't miss out on reading this paper:",
    "I'm off to find the next paper to share, but make sure you take a look at this one:",
]
