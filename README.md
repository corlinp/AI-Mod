# AI-Mod


AI Mod is a modular social media content scanning system made to detect spam, trolling, doxing, and more. While designed to be a smarter version of Reddit's Automoderator, it is flexible enough to be used with any platform.

Test out a live demo at https://ai-mod.com


## Features

This table highlights categories that AI mod currently detects.

Detected | Posts | Comments | Users |
---|---|----|----|
Link Flair | Planned |  | |
Spam | Active | Active | Active |
NSFW | Links Only | Links Only | |
Trolling | Active | Active | Active |
Doxxing | Planned | Planned | |
Rule Breaking | Planned | Planned | Planned |
Bots |   |   | Planned |
Reposts |  |  |  |


## Running AI Mod

If you're a Reddit moderator interested in using AI Mod on your subreddit, please use [this form](https://docs.google.com/forms/d/1bC1D5yZNeNCMvZkXWH8pig6Uz6DPfngBr3H2FrHj6aI/) to register your interest.

If you're interested in using AI Mod in another way, such as writing an adapter for another social platform, post in the [AI Mod Discord](https://discord.gg/v72rkzP) for assistance.

If you'd like to run AI Mod yourself, you must fill out a `secrets.json` file with various API Keys and endpoints. See `secrets.sample.json` for the format. Then, with Redis open, run the desired Python file. You can also boot up the API in Docker with `make start`

### API
This repo contains the code necessary to host an API and website using a tornado webserver.

### Reddit
The Reddit folder contains the tools necessary to scan Reddit and perform mod actions on each post according to individual subreddit configurations.

## Content Categories

AI Mod's content analysis functionality is simple. Pass in a string and AI Mod will return a dictionary of categories for which is has rated its confidence. We call this a scorecard.

### Spam

AI Mod uses a vast dataset of more than 850,000 Reddit spam posts. This is assembled from every single post and comment made by every user ever posted to /r/spam (before it closed). The data was filtered for accuracy and used to train a classifier.

### Trolling

AI Mod's trolling datasets are assembled from hand-annotated datasets from Kaggle and Wikipedia.

This is combined with a dataset of profane words and a custom fuzzy-matching model that can account for intentional misspellings and letter/number substitutions.

### Doxing

AI Mod detects Doxing by identifying possible Emails, Phone Numbers, and IP Addresses. This is combined with intelligent web searches to determine if posted personal information is public or not.

### Bots

AI Mod is able to detect other bots by analyzing their active hours, word use, and average time to respond.

## Special Thanks

Thanks to Jason Baumgartner ([/u/stuck_in_the_matrix](https://www.reddit.com/user/stuck_in_the_matrix)) of Pushshift.io for providing Reddit data APIs used in training and running AI Mod, and for loaning server time to host AI Mod.

Thanks to [/u/thecodingdude](https://www.reddit.com/user/thecodingdude) for providing feedback and coding up some upcoming subreddit onboarding pages.

Finally, thanks to the moderators of all other subreddits I've done testing on for providing valuable feedback.

* /r/datasets
* /r/BuyItForLife
* /r/UCSD
* /r/ProceduralGeneration
