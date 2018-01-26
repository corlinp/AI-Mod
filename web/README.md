# AI Mod Website

The AI Mod website is served by Tornado from api_main.py in the
src folder.


## API

Allowing each classifier to accept an arbitrary string gives the
possibility of using it as a general content moderation service, either
hosted or as a microservice within another platform. The AI Mod API
allows any developer to take advantage of its capabilities.

### Usage

`POST` some text to /api

*Returns*: A JSON string with confidence for each category and possibly
some notes. Example:

    {
       "nsfw":0.25,
       "spam":0.92,
       "notes":["Contains Swear Words"]
    }

Note that Flair and Rule-Breaking detection are not supported as they are
subreddit specific.