from setuptools import setup


setup(
    name='blog',
    version='0.1',
    install_requires=[
        # Web
        'tornado==3.2',
        'MarkupSafe==0.19',
        'Jinja2==2.7.2',
        'WTForms==1.0.5',

        # Database
        'SQLAlchemy==0.9.2',
        'psycopg2==2.5.2',
        'PyMySQL==0.6.1',

        # Misc.
        'passlib==1.6.2',
        'Markdown==2.4'
    ]
)
