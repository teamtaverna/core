[![Coverage Status](https://coveralls.io/repos/github/teamtaverna/core/badge.svg?branch=master)](https://coveralls.io/github/teamtaverna/core?branch=master) [![Build Status](https://travis-ci.org/teamtaverna/core.svg?branch=master)](https://travis-ci.org/teamtaverna/core)

# CORE
Core is the power house of FoodBoard app, an open source meal review and management platform. More information can be found on the [wiki](https://github.com/teamtaverna/assets/wiki). You can download the latest release [here](https://github.com/teamtaverna/core/releases/latest).

### Tech
Core is written in Python3 and Django 1.11.

### Collaboration

Want to contribute? Great!

You need to have postgreSQL installed and set up on your machine.

Fork the repository. Please read the CONTRIBUTING.md guide.

### Installation

**Mac Users**

Be sure to have the following installed and setup first.
* Python 3
* PostgreSQL (Ensure the server is running)
* Brew
* Xcode

Next,
* Install [Virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/install.html).
* Create a virtual environment for the project.
    ```
    mkvirtualenv <envname>
    ```

* Use the flag `-p python3` if you also have python 2 installed
    ```
    mkvirtualenv -p python3 <envname>
    ```

* Install requirements in the virtual environment created
    ```
    pip install -r requirements.txt
    ```

* Create a database with PostgreSQL.
* Create a `.env` file and copy the contents of `.env.example` file to it.
* Replace
  - `DB_NAME` with the name of your database,
  - `DB_USER` with your database user name,
  - `DB_PASSWORD` with your database password,
  - `SECRET_KEY` with the value gotten when you run this script in the terminal `python3 scripts/secret_key_gen.py`.

* Run database migrations with this command
    ```
    python3 manage.py migrate
    ```

* Run server to ensure everything is working fine.
    ```
    python3 manage.py runserver
    ```


To run tests
```
$ python manage.py test
```
```
$ flake8 .
```
