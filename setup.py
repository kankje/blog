from setuptools import setup


setup(
    name='blog',
    version='1.0.0',
    author='Jere Kankaanranta',
    author_email='jere@kankje.com',
    install_requires=[
        # Tests
        'nose==1.3.1',

        # Web
        'Flask==0.10.1',
        'Flask-WTF==0.9.5',
        'Flask-SQLAlchemy==1.0',
        'psycopg2==2.5.2',
        'PyMySQL==0.6.1',
        'redis==2.9.1',

        # Misc.
        'passlib==1.6.2',
        'Markdown==2.4'
    ]
)
