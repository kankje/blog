blog
====

Introduction
------------

A simple blog platform, written in Python.

Requirements
------------

* Python 3, pip and virtualenv
* PostgreSQL server and redis
* nginx and uwsgi

Database setup
--------------

`$ psql -U postgres`

    CREATE DATABASE blog;
    \c blog
    CREATE SCHEMA blog;
    CREATE ROLE blog WITH LOGIN PASSWORD 'password';
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA blog TO blog;

Installation
------------

1. Set up the database
2. Change the working directory to the install directory: `$ cd /var/www`
3. Clone the repository: `$ git clone git@github.com:kankje/blog.git`
4. Copy and edit the config files accordingly:
    * `$ cp docs/config/example.config.py app/config.ini`
    * `$ cp docs/config/example.nginx.conf /etc/nginx/conf.d/blog.conf`
    * `$ cp docs/config/example.nginx.site /etc/nginx/conf.d/blog.site`
    * `$ cp docs/config/example.init.d.script /etc/init.d/blog`
5. Create a virtualenv: `$ virtualenv venv`
6. Activate the virtualenv: `$ source venv/bin/activate`
7. Install the dependencies: `$ python setup.py install`
8. Start the blog service: `$ service blog start`
9. Visit `https://your-blog.com/admin/install`
10. After the installation, you can log in using `https://your-blog.com/admin/login`

For developers
==============

* [PEP-8](http://legacy.python.org/dev/peps/pep-0008/)
* You can run tests by running `$ nosetests` in the project root.
