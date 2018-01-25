# Contributing to AI Mod

I encourage anyone interested in this project to contribute.
There are many ways large and small to help out;
from creating content classifiers to adding new swear words
to the filter. This document provides some guidance.

## Development Guidelines

The general structure of AI Mod's content classification is to bring
together multiple separate 'classifiers' that determine if a text
string is nsfw / spam / etc and a master method to combine all of those
reports into one.

On top of that we have a web-facing API and a Reddit interface that
both make use of those reports. If you want to contribute to AI Mod
 here are a few suggestions:

* Adding Classifiers
* Extending the Reddit interface
* Improving the ai-mod.com website
* Integrating third party APIs and libraries

### Adding New Classifiers

A classifier takes an arbitrary string and returns returns some data
about it, specifically the confidence / probability (0.0 to 1.0) that it
 falls into one or more categories, and maybe a few notes.

So in order to easily integrate many classifiers, I'm requiring that they
all return a string like the following:

    {
       "nsfw":0.25,
       "spam":0.92,
       "notes":["Contains Swear Words"]
    }

The proposed categories are `notes`, `nsfw`, `spam`, `troll`, `doxx`,
 `rules`, `bot`, `repost`, `other`

A string to be analyzed will be run through every classifier and
combined. If multiple classifiers output info in the same category,
their notes will be combined and confidence taken from the highest one.

Let's look at a very basic classifier, this will classify your text as
NSFW if it contains the word "shit":

    def detect_nsfw_language(text):
        report = {'nsfw': 0.0, 'notes':[]}
        if "shit" in text:
            report['nsfw'] = 1.0
            report['notes'].append("NSFW Language Detected!")
    return report

Now I'll add the method to the `analysis_methods` array in `text_analysis.py` and run this string:

`analyze_text("You're full of shit")`

 > {'notes': ['NSFW Language Detected!'], 'nsfw': 1.0}

And there you have it. It's integrated with the collective.
