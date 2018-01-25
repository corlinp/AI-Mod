# Development Notes

Things that I have attempted and either failed or decided against.

## Text Classifiers

I have tested Facebook's FastText, a probabilistic word-frequency classifier, and a Keras Neural Network model. None have been able to match the accuracy of the SKLearn implementation currently in classifiers/sklearn_text_classifier.py.

## NSFW Image Recognition

I have tested Nudepy and [Yahoo!'s Open NSFW](https://github.com/yahoo/open_nsfw) models. Both had an alarmingly high false-positive rate so I have decided against using NSFW image detection for the time being.


