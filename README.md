Master: [![Build Status](https://travis-ci.com/codethesaurus/codethesaur.us.svg?branch=master)](https://travis-ci.com/codethesaurus/codethesaur.us)
Develop: [![Build Status](https://travis-ci.com/codethesaurus/codethesaur.us.svg?branch=develop)](https://travis-ci.com/codethesaurus/codethesaur.us)

## [codethesaur.us](http://codethesaur.us/)
Website that will compare language features side by side.

## Why would you want this?
Good question. If there's an aspect of a language you don't know, you can compare a languages you know with a language you do. It's a good way to quickly learn a new language, or use it as a quick reference to remember things by.

## Requirements

* Python 3.x
* Django 3.11

If you run `python --version` and it shows Python 2.x but you know you have
Python 3.x installed, you may need to suffix all `python` and `pip` commands
with `3`, e.g. `pip3` and `python3`, or follow the process for making Python
3 your default Python installation.

## Cloning and running it locally

1. Clone the project (`git clone https://github.com/codethesaurus/codethesaur.us.git`)
1. Install [Python](https://www.python.org/downloads/)
1. For ease of use, make sure your Python folder is in your `PATH` environment variable
1. Run `pip install -r requirements.txt`
1. Then run `python manage.py runserver`
1. In your browser, visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) or [http://localhost:8000/](http://localhost:8000/)
1. Press CTRL+C in the terminal to stop the server.

## Code of Conduct

All contributors are required to follow the [Code Thesaurus Code of Conduct](CODE_OF_CONDUCT.md).

## Questions?

Preferred: Reach out on Twitter [@codethesaurus](https://twitter.com/codethesaurus)

You could also email the core team (coreteam@codethesaur.us).
