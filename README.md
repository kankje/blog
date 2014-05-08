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

Installation
------------

1. Set up the database
    * `CREATE ROLE blog WITH LOGIN PASSWORD 'password';`
    * `CREATE DATABASE blog WITH OWNER blog;`
2. Change the working directory to the install directory: `$ cd /var/www`
3. Clone the repository: `$ git clone git@github.com:kankje/blog.git`
4. Copy and edit the config files accordingly:
    * `$ cp docs/config/example.config.py app/config.py`
    * `$ cp docs/config/example.nginx.conf /etc/nginx/sites-available/blog`
    * `$ ln -s /etc/nginx/sites-available/blog /etc/nginx/sites-enabled/blog`
    * `$ cp docs/config/example.uwsgi.ini /etc/uwsgi/apps-available/blog.ini`
    * `$ ln -s /etc/uwsgi/apps-available/blog.ini /etc/uwsgi/apps-enabled/blog.ini`
5. Create a virtualenv: `$ virtualenv venv`
6. Activate the virtualenv: `$ source venv/bin/activate`
7. Install the dependencies: `$ python setup.py install`
8. Start the blog service: `$ service blog start`
9. Visit `https://your-blog.com/admin/install`
10. After the installation, you can log in using `https://your-blog.com/admin/login`

For developers
==============

* For code conventions check out [PEP-8](http://legacy.python.org/dev/peps/pep-0008/)
* To run tests, run `$ nosetests` in project root
