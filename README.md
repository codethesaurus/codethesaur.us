## [codethesaur.us](http://codethesaur.us/)
Website that will compare language features side by side.

## Why would you want this?
Good question. If there's an aspect of a language you don't know, you can compare a languages you know with a language you do. It's a good way to quickly learn a new language, or use it as a quick reference to remember things by.

## Requirements

* Python 3.x
* Django 3.11
* PostgreSQL 13.x

If you run `python --version` and it shows Python 2.x but you know you have
Python 3.x installed, you may need to suffix all `python` and `pip` commands
with `3`, e.g. `pip3` and `python3`, or follow the process for making Python
3 your default Python installation.

## Cloning and running it locally

### Windows

1. Clone the project (`git clone https://github.com/codethesaurus/codethesaur.us.git`)
1. Switch into to directory `cd codethesaur.us`
1. Check to see if Python 3.x is installed with `python --version` or `python3 --version`. If Python 3.x isn't installed, visit https://www.python.org/downloads/windows/ or install it with `choco install python`
1. Install Python's virtual environment venv with the command `pip3 install virtualenv`
1. To set up new virtual environment, run `virtualenv venv`
1. To activate virtual environment, run `venv\Scripts\activate.bat`
1. Run `pip install -r requirements.txt`
1. Then Run `python manage.py runserver`
1. In your browser, visit `http://127.0.0.1:8000/` or `http://localhost:8000/`
1. Press CTRL+C in the terminal to stop the server
1. To deactivate the virtual environment, run `venv\Scripts\deactivate.bat`

### Mac

1. Check to see if Python 3.x is installed with `python --version` or `python3 --version`. If Python 3.x isn't installed, install it with `brew install python`
1. Clone the project (`git clone https://github.com/codethesaurus/codethesaur.us.git`)
1. Switch into to directory `cd codethesaur.us`
1. Run `pip3 install virtualenv`
1. To set up new virtual environment, run `virtualenv --no-site-packages venv`
1. To activate virtual environment, run `source venv/bin/activate`
1. Run `pip3 install -r requirements.txt`
1. Then Run `python3 manage.py runserver`
1. In your browser, visit `http://127.0.0.1:8000/` or `http://localhost:8000/`
1. Press CTRL+C in the terminal to stop the server
1. To deactivate the virtual environment, run `deactivate`

### Linux 

1. If python3 and pip3 are not installed there is a guide for [Linux systems](https://www.tecmint.com/install-pip-in-linux/)
1. Check system default `python --version`
   If the returned text is not python 3.x then using `python3` will be required for following steps
   Or if you would like to set python3 as a default simply open your .bashrc file.
   `sudo nano ~/.bashrc` and add `alias python='python3'`
1. Django 3.11 can be installed using the pip3 package manager.
   `pip3 install django==3.11`
1. Install PostgreSQL `sudo apt install -y postgresql` - Debian
1. Install venv for virtual environment
   `sudo apt install -y python3-venv` - Debian
    Full python3 and venv setup [centOS](https://www.i2tutorials.com/how-to-install-python-set-up-programming-environment-on-centos/)
1. Clone the project (`git clone https://github.com/codethesaurus/codethesaur.us.git`)
1. Switch into to directory `cd codethesaur.us`
1. Use directory as virtual environment `python3 -m venv codethesaur.us`
1. Activate the directory `source codethesaur.us/bin/activate`
1. Run `pip install -r requirements.txt`
1. Then run `python manage.py runserver`
1. In your browser, visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) or [http://localhost:8000/](http://localhost:8000/)
1. Press CTRL+C in the terminal to stop the server.

### Docker container

If you want, you can run and develop the application within docker container. To do this, firstly you have to make sure that you have docker installed and running on you local machine. If you don't, [here](https://docs.docker.com/get-docker/) you can see how to get it.
To build the app inside a docker container, follow the following steps:

1. Firstly, build the docker image based on the supplied Dockerfile `docker build -t cthesaurus-img .`
1. Then, run the docker container by using the image that you've just created `docker run --name codethesaurus-container -dti -p 8000:8000 -v \`pwd\`:/code cthesaurus-img bash`
1. You can check if the container is up and running by invoking 'docker container ls' - your container should be present on the list, its name should be set to "codethesaur-container".
1. Now you can attach to running container by using the following command `docker attach codethesaurus-container`
1. When you are attached, you have access to command line interface which controls the container. From there, you can manage your django app by manage.py, as you would do in local environment. 
1. To run the server, simply run `python manage.py runserver 0:8000` - you have to specify 0.0.0.0 (0 is a shortcut for that) address to be able to access the website outside of the container - it is possible thanks to the port mapping, which is set during 'docker run ...' command by specifying '-p 8000:8000'.
1. To edit the respository, do it in your local directory on your machine - the changes that you make will be refleced in the container, thanks to the mounting of the filesystem, which was specified by '-v pwd:/code' option during 'docker run ...' command execution.

## Contributing

Check out the [Contributing Guide](CONTRIBUTING.md) to learn more about how you can help add more language data, fix bugs, or add features!

## Code of Conduct

All contributors are required to follow the [Code Thesaurus Code of Conduct](CODE_OF_CONDUCT.md).

## Questions?

Preferred: Reach out on Twitter [@codethesaurus](https://twitter.com/codethesaurus)

You could also email the core team (coreteam@codethesaur.us).
