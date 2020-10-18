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

** Windows **

1. Check to see if Python 3.x is installed with `python --version` or `python3 --version`. If Python 3.x isn't installed, visit https://www.python.org/downloads/windows/ or install it with `choco install python`
1. Install Python's virtual environment venv with the command `pip3 install virtualenv`
1. To set up new virtual environment, run `virtualenv venv`
1. To activate virtual environment, run `venv\Scripts\activate.bat`
1. Run `pip install -r requirements.txt`
1. Then Run `python manage.py runserver`
1. In your browser, visit `http://127.0.0.1:8000/` or `http://localhost:8000/`
1. Press CTRL+C in the terminal to stop the server
1. To deactivate the virtual environment, run `venv\Scripts\deactivate.bat`

**Linux deployment:**

1. If python3 and pip3 are not installed there is a guide for [Linux systems](https://www.tecmint.com/install-pip-in-linux/)
1. Check system default `python --version`
   If the returned text is not python 3.x then using `python3` will be required for following steps
   Or if you would like to set python3 as a default simply open your .bashrc file.
   `sudo nano ~/.bashrc` and add `alias python='python3'`
1. Django 3.11 can be installed using the pip3 package manager.
   `pip3 install django==3.11`

**Run using venv**
1. Install venv for virtual environment
   `sudo apt install -y python3-venv` - Debian
    Full python3 and venv setup [centOS](https://www.i2tutorials.com/how-to-install-python-set-up-programming-environment-on-centos/)
1. Clone the project (`git clone https://github.com/codethesaurus/codethesaur.us.git`)
1. Switch into to directory `cd codethesaur.us`
1. Use directory as virtual environment `python3 -m venv codethesaur.us`
1. Activate the directory `source codethesaur.us/activate`
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

## For mac users

1. Clone the project (`git clone https://github.com/codethesaurus/codethesaur.us.git`)
1. Run `pip3 install virtualenv`
1. To set up new virtual environment, run `virtualenv --no-site-packages venv`
1. To activate virtual environment, run `source venv/bin/activate`
1. Run `pip install -r requirements.txt`
1. Then Run `python manage.py runserver`
1. In your browser, visit `http://127.0.0.1:8000/` or `http://localhost:8000/`
1. Press CTRL+C in the terminal to stop the server
1. To deactivate the virtual environment, run `deactivate`


## Code of Conduct

All contributors are required to follow the [Code Thesaurus Code of Conduct](CODE_OF_CONDUCT.md).

## Questions?

Preferred: Reach out on Twitter [@codethesaurus](https://twitter.com/codethesaurus)

You could also email the core team (coreteam@codethesaur.us).
