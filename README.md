[![Coverage Status](https://coveralls.io/repos/github/teamtaverna/taverna_api/badge.svg?branch=master)](https://coveralls.io/github/teamtaverna/taverna_api?branch=master)

# Taverna API
Taverna API is the power house of Taverna app, an open source meal review and management platform.

### Tech
Taverna API is written in Python3 and Django 1.9.

### Collaboration

Want to contribute? Great!

You need to have postgreSQL installed and set up on your machine.

Clone the repository from [GitHub](https://www.github.com)
```
git clone https://github.com/teamtaverna/taverna_api.git
```

### Installation

**Mac Users**

Be sure to have the following installed and setup first.
* PostgreSQL (Ensure the server is running)
* Brew
* Xcode

Next, step into the project directory and set up your environment by running this script.

```
./scripts/local_env_setup.sh
```

**OR follow these steps to set up manually.**
* Install [Virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/install.html).
* Create a virtual environment for the project.
* Install requirements in the virtual environment created
    ```
    pip install -r requirements.txt
    ```
* Create a database with PostgreSQL.
* Create a `.env` file and copy the contents of `.env.example` file to it.
* Replace the `DB_NAME` with the name of your database, and `SECRET_KEY` with the value gotten when you run this script in the terminal `python3 scripts/secret_key_gen.py`.
* Run database migrations with this command
    ```
    python3 manage.py migrate
    ```
* Run server to ensure everything is working fine.
    ```
    python3 manage.py runserver
    ```
