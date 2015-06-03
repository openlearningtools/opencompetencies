<a name="top"></a>Open Competencies
===

Sections
---
- [Vision](#vision)
- [Setting up a local development version](#dev_setup)
- [Glossary](#glossary)
- [License](#license)
- [About](#about)

<a name="vision"></a>Vision
-------
[Open Competencies](http://opencompetencies.org) allows individuals and groups to build their own sets of education standards.

The full version of Open Competencies will allow educators to fork any existing set of standards, and share sets of standards freely. For example, if you like the standards my school works with, you can fork my school's set of standards and then revise them as you see fit. If your school's science standards are better than mine, I can import your school's science standards and begin working with them immediately. There are many benefits to this approach to building sets of standards.

The full version of Open Competencies will also include an integrated instructional planning tool. There are a number of approaches to building standards-based instructional units, and educators shouldn't have to do this in Word, or in proprietary planning tools.

[top](#top)

<a name="dev_setup"></a>Setting up a local development version
---
Instructions at this point are based on an Ubuntu development environment, or something similar. You may need some system-wide tools installed. If you have any questions about setting up a local development environment for this project, please [open an issue](https://github.com/openlearningtools/opencompetencies/issues/new).

Go to a directory where you want to work with this project, clone the repository, and cd into the new directory:

    $ cd /srv
    /srv $ git clone https://github.com/openlearningtools/opencompetencies
    /srv $ cd opencompetencies

Create a virtual environment called venv, and install requirements:

    /srv/opencompetencies $ virtualenv venv
    /srv/opencompetencies $ source venv/bin/activate
    (venv)/srv/opencompetencies $ pip install -r requirements.txt

Create a database for this project.  The settings, and some of the documentation assume you are using postgres.

    CREATE DATABASE opencompetencies_db OWNER db_username ENCODING 'utf8'

Set the DATABASE_URL environment variable.  If you want to turn on debugging, set the DJANGO_DEBUG environment variable.  If you are going to work on this project, you can make these settings part of your venv/bin/activate script, and they will be set each time you activate the venv. You will also need to set a DJANGO_SECRET_KEY environment variable.

    (venv)/srv/opencompetencies $ export DATABASE_URL=postgres://db_username:password@localhost/opencompetencies_db
    (venv)/srv/opencompetencies $ export DJANGO_DEBUG=True
    (venv)/srv/opencompetencies $ export DJANGO_SECRET_KEY=your_secret_key

Run `migrate`, create a superuser and connect it to a user profile, and start the development server:

    (venv)/srv/opencompetencies $ python manage.py migrate
    (venv)/srv/opencompetencies $ python manage.py shell
    >>> from competencies.models import UserProfile
    >>> from django.contrib.auth.models import User
    >>> su = User.objects.get(id=1)
    >>> new_userprofile = UserProfile()
    >>> new_userprofile.user = su
    >>> new_userprofile.save()
    (venv)/srv/opencompetencies $ python manage.py runserver

Visit [http://localhost:8000](http://localhost:8000), and verify that your local deployment works.

To avoid having to set the environment variables each time you open this project, you can have the virtual environment's activate script do it for you.  Create a file called .env, in /srv/opencompetencies:

    (venv)/srv/opencompetencies $ touch .env

Add the following lines to .env:

    DATABASE_URL=postgres://db_username:password@localhost/opencompetencies_db
    DJANGO_DEBUG=True
    DJANGO_SECRET_KEY=your_secret_key

Add the following lines to the end of /venv/bin/activate:

    # Use my env variables:
    export $(cat /srv/opencompetencies/.env)

Now these environment variables will be loaded each time you activate your virtual environment.  Both the .env file and the venv/ directory are listed in .gitignore, so neither will be committed in your local repository.

[top](#top)

<a name="glossary"></a>Glossary
---
There's a brief [glossary](https://github.com/openlearningtools/opencompetencies/blob/master/docs/GLOSSARY.md) of relevant terms included in the docs directory.

<a name="license"></a>License
---
Open Competencies is released under the [MIT license](https://github.com/openlearningtools/opencompetencies/blob/master/LICENSE.txt).

[top](#top)

<a name="about"></a>About
---
Open Competencies is being developed by Eric Matthes (ehmatthes). If you would like to get in touch feel free to send me an email at ehmatthes@gmail.com, or find me on twitter <a href="http://twitter.com/ehmatthes">@ehmatthes</a>.

[top](#top)
