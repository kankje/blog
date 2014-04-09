blog
====

Introduction
------------

A simple blog platform, written in Python.

Requirements
------------

* Python 3, pip and virtualenv
* PostgreSQL or MySQL server
* Web server, e.g. nginx
    * It is possible to run the blog by itself or on other HTTP servers,
      but nginx is recommended and example config for other servers is not included

Database setup
--------------

PostgreSQL

    CREATE DATABASE blog;
    \c blog
    CREATE ROLE blog WITH PASSWORD 'password';
    CREATE SCHEMA blog;
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA blog TO blog;

MySQL

    CREATE DATABASE blog;
    USE DATABASE blog;
    GRANT ALL PRIVILEGES ON blog TO blog@localhost IDENTIFIED BY 'password';

Installation
------------

1. Set up the database
2. Change the working directory to the install directory: `$ cd /var/www`
3. Clone the repository: `$ git clone git@github.com:kankje/blog.git`
4. Copy and edit the config files accordingly:
    * `$ cp docs/config/example.app.ini config/app.ini`
    * `$ cp docs/config/example.nginx.conf /etc/nginx/conf.d/blog.conf`
    * `$ cp docs/config/example.upstart.conf /etc/init/blog.conf`
5. Create a virtualenv: `$ virtualenv venv`
6. Activate the virtualenv: `$ source venv/bin/activate`
7. Install the dependencies: `$ python setup.py install`
8. Start the blog service: `$ start blog`
9. Visit `https://your-blog.com/install`
10. After the installation, you can log in using `https://your-blog.com/login`

For developers
==============

* You can run tests by running `$ nosetests` in the project root.
