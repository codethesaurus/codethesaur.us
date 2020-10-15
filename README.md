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

**Linux deployment:**

Optional installation guides:

Install python3 and pip3 for [linux systems](https://www.tecmint.com/install-pip-in-linux/)

django installation
`pip3 install django`

Recommended for use with python 3.6 and later
Install venv for virtual environment (optional)
`sudo apt install -y python3-venv` - Debian
Full python3 and venv setup [centOS](https://www.i2tutorials.com/how-to-install-python-set-up-programming-environment-on-centos/)

Recommended for use with python 3.3 and 3.5 deprecated in python 3.6
Install [pyenv](https://www.tecmint.com/pyenv-install-and-manage-multiple-python-versions-in-linux/) (optional)
Be sure to install a python3 version in pyenv.

**Run using venv**

1. Clone the project (`git clone https://github.com/codethesaurus/codethesaur.us.git`)
1. Switch into to directory `cd codethesaur.us`
1. Use directory as virtual environment `python3 -m venv codethesaur.us`
1. Activate the directory `source codethesaur.us/activate`
1. Run `pip install -r requirements.txt`
1. Then run `python manage.py runserver`
1. In your browser, visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) or [http://localhost:8000/](http://localhost:8000/)
1. Press CTRL+C in the terminal to stop the server.

**Run using pyenv**

1. Clone the project (`git clone https://github.com/codethesaurus/codethesaur.us.git`)
1. Switch into to directory `cd codethesaur.us`
1. Use directory as virtual environment use your current version in place of 3.x, omit if system default is set to python 3.x `pyenv virutalenv 3.x venv_codethesaur.us`
1. Activate the directory `pyenv activate venv_codethesaur.us`
1. Run `pip install -r requirements.txt`
1. Then run `python manage.py runserver`
1. In your browser, visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) or [http://localhost:8000/](http://localhost:8000/)
1. Press CTRL+C in the terminal to stop the server.

**Run with no virtual environment**

1. Clone the project (`git clone https://github.com/codethesaurus/codethesaur.us.git`)
1. switch into to directory `cd codethesaur.us`
1. Run `pip install -r requirements.txt`
1. Then run `python manage.py runserver`
1. In your browser, visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) or [http://localhost:8000/](http://localhost:8000/)
1. Press CTRL+C in the terminal to stop the server.

## Code of Conduct

All contributors are required to follow the [Code Thesaurus Code of Conduct](CODE_OF_CONDUCT.md).

## Questions?

Preferred: Reach out on Twitter [@codethesaurus](https://twitter.com/codethesaurus)

You could also email the core team (coreteam@codethesaur.us).
