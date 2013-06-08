<a name="top"></a>Open Competencies
===

Sections
---
- [Vision](#vision)
- [Setting up your own development version on heroku](#dev_setup)
- [Pre-coding decisions](#pre_coding_decisions)
- [About](#about)

<a name="vision"></a>Vision
-------
Open Competencies is a dynamic list of all the information you could learn.  It is a tree of knowledge, with different relationships identified between all of the bits of knowledge.

How do you use it?  Let's say you want to be a professional programmer.  You click a button, and all of the bits of knowledge needed to be a programmer light up.  You realize you don't just want to be a programmer.  You  also want to write really well, not just about technical topics.  So you click a few buttons that describes how you want to use writing in your life.  All of the bits that relate to writing well light up.

A separate tool will let you take a copy of your learning targets, and track your progress in learning them.  That needs to be a separate tool, because it requires a different kind of security model.

More information is included in the [VISION.md](https://github.com/openlearningtools/opencompetencies/blob/master/docs/VISION.md) document.

[top](#top)

<a name="dev_setup"></a>Setting up your own development version on heroku
---
You can see a live version of this project at [http://opencompetencies.herokuapp.com](http://opencompetencies.herokuapp.com), as long as it does not get clobbered because it's on a free tier.  If you want to ask questions or discuss the project, feel free to share your thoughts in issue 2, [Initial Feedback and Discussion](https://github.com/openlearningtools/opencompetencies/issues/2).

Instructions at this point are based on an Ubuntu development environment, or something similar. You may need some system-wide tools installed, which we can help clarify if you need. If you have any questions about setting up a local development environment for this project, please visit issue 1, [Installation Questions](https://github.com/openlearningtools/opencompetencies/issues/1).

### Set up a local development environment:
Go to a directory where you want to work with this project, and clone the repository, and cd into the new directory:

    $ cd /srv
    /srv $ git clone https://github.com/openlearningtools/opencompetencies
    /srv $ cd opencompetencies

Create a virtual environment called venv, and install requirements:

    /srv/opencompetencies $ virtualenv --distribute venv
    /srv/opencompetencies $ source venv/bin/activate
    (venv)/srv/opencompetencies $ pip install -r requirements.txt

Create a database for this project.  The settings, and some of the documentation assume you are using postgres.

    $ su postgres
    $ psql template1
    template1=# CREATE DATABASE opencompetencies_db OWNER db_username ENCODING 'utf8';
	 template1=# \q
	 $ su comp_username

Set the DATABASE_URL environment variable.  If you want to turn on debugging, set the DJANGO_DEBUG environment variable.  If you are going to hack on this project, you can make these settings part of your venv/bin/activate script, and they will be set each time you activate the venv. You will also need to set a DJANGO_SECRET_KEY environment variable.

    (venv)/srv/opencompetencies $ export DATABASE_URL=postgres://db_username:password@localhost/opencompetencies_db
    (venv)/srv/opencompetencies $ export DJANGO_DEBUG=True
    (venv)/srv/opencompetencies $ export DJANGO_SECRET_KEY=your_secret_key

Run syncdb, create a superuser, migrate competencies, and start the development server:

    (venv)/srv/opencompetencies $ python manage.py syncdb
    (venv)/srv/opencompetencies $ python manage.py migrate competencies
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

Now these environment variables will be loaded each time you activate your virtual environment.  Both the .env file and the venv/ directory are included in .gitignore, so neither will be committed in your local repository.

### Deploy your test version to heroku:
If you have not done so already, create a heroku account and install the heroku toolbelt. The [following command](https://toolbelt.heroku.com/) will install the heroku toolbelt on ubuntu:

    $ wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh

Make sure you are logged in to heroku through the command line.  Then in your local project directory, activate the virtual environment and run "heroku create". After heroku creates your project, push your files to heroku:

    $ heroku login
    $ cd /srv/opencompetencies
    /srv/opencompetencies $ source venv/bin/activate
    (venv)/srv/opencompetencies $ heroku create
    (venv)/srv/opencompetencies $ git push heroku master

Now we need to set our DJANGO_SECRET_KEY environment variable:

    $ heroku config:set DJANGO_SECRET_KEY="your_secret_key"

After this, you will need to sync the development database on heroku.

    (venv)/srv/opencompetencies $ heroku run bash
    $ python manage.py syncdb
    $ python manage.py migrate competencies
    $ exit
    (venv)/srv/opencompetencies $ heroku open

If you can run commands locally, but have trouble with "heroku run bash", you can run those commands individually through the command line:

    (venv)/srv/opencompetencies $ heroku run python manage.py syncdb
    (venv)/srv/opencompetencies $ heroku run python manage.py migrate competencies
	 (venv)/srv/opencompetencies $ heroku open

This should take you to your own live version of the opencompetencies project. When you make changes to your local project and you want to push those changes live, just push your changes to heroku:

    (venv)/srv/opencompetencies $ git push heroku master

If you are new to using heroku with django projects, take a look at the [heroku django](https://devcenter.heroku.com/articles/django) page.

[top](#top)

<a name="pre_coding_decisions"></a>Pre-coding decisions
---
A number of decisions need to be made before we write any code, beyond the demo code that has already been written:
- Agree on the overall scope of this project, as laid out in the [Vision](https://github.com/openlearningtools/opencompetencies/blob/master/docs/VISION.md) and [Use Cases](https://github.com/openlearningtools/opencompetencies/blob/master/docs/VISION.md#use_cases) sections.
- Write any additional functional specs needed before coding.
- Agree on a taxonomy for the hierarchy of learning targets.
- Ensure the taxonomy is trademark-free, and designate an appropriate open license for the taxonomy.
- Agree on an overall approach to identifying the kinds of relationships between different pieces of knowledge?
- [(done)](https://github.com/openlearningtools/opencompetencies/blob/master/docs/GLOSSARY.md) Write a glossary for the first few levels in the taxonomy
- Move much of this file to a wiki? May be better than current /docs folder setup.
- Agree on which framework to use

[top](#top)
<a name="about"></a>About
---
Open Competencies is currently being developed by Eric Matthes (ehmatthes). If you would like to get in touch feel free to send me an email at ehmatthes@gmail.com, or find me on twitter <a href="http://twitter.com/ehmatthes">@ehmatthes</a>.

If you would like to support development of Open Competencies, please consider supporting me on Gittip:

[![Gittip](http://badgr.co/Gittip/ehmatthes.png)](https://www.gittip.com/ehmatthes/)

[top](#top)
