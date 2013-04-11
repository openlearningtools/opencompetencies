<a name="top"></a>Open Competencies
===

Sections
---
- [Vision](#vision)
- [Setting up your own development version on heroku](#dev_setup)
- [Pre-coding decisions](#pre_coding_decisions)

<a name="vision"></a>Vision
-------
Open Competencies is a dynamic list of all the information you could learn.  It is a tree of knowledge, with different relationships identified between all of the bits of knowledge.

How do you use it?  Let's say you want to be a professional programmer.  You click a button, and all of the bits of knowledge needed to be a programmer light up.  You realize you don't just want to be a programmer.  You  also want to write really well, not just about technical topics.  So you click a few buttons that describes how you want to use writing in your life.  All of the bits that relate to writing well light up.

A separate tool will let you take a copy of your learning targets, and track your progress in learning them.  That needs to be a separate tool, because it requires a different kind of security model.

More information is included in the [VISION.md](https://github.com/openlearningtools/opencompetencies/blob/master/docs/VISION.md) document.

[top](#top)

<a name="dev_setup"></a>Setting up your own development version on heroku
---
You can see a live version of this project at [http://opencompetencies.herokuapp.com](http://opencompetencies.herokuapp.com), as long as it does not get clobbered because it's on a free tier.

Instructions at this point are based on an Ubuntu development environment, or something similar.

Set up a local development environment:
- Make a directory to hold the project, and change into that directory.
- Clone this repository:
    - git clone https://github.com/openlearningtools/opencompetencies
- Change into the opencompetencies directory.
- Create a virtual environment called venv using requirements.txt, and activate the environment:
    - virtualenv --distribute venv
    - sudo pip install -r requirements.txt
    - source venv/bin/activate
- Create a database for this project.  This documentation assumes you are using postgres.
- Set the DATABASE_URL environment variable:
    - DATABASE_URL=postgres://database_user:password@localhost/database_name
- If you would like to turn on debugging, add a DEBUG environment variable.
    - DEBUG=True
- run syncdb, and fake migrations
    - python manage.py syncdb
	 	  - create a superuser, following prompts
    - python manage.py migrate --fake competencies
- visit http://localhost:8000, and verify the site works

Set up your own test version on heroku:
- If you have not done so already, create a heroku account and install the heroku toolbelt.
- In your local project directory, run "heroku create"
- You will need to set up the database on heroku:
    - heroku run bash
    - python manage.py syncdb
    - python manage.py migrate competencies
- heroku open
- You should have a working development version on heroku.

[top](#top)

<a name="pre_coding_decisions"></a>Pre-coding decisions
---
A number of decisions need to be made before we write any code:
- Agree on the overall scope of this project, as laid out in the [Vision](#vision) and [Use Cases](#use_cases) sections.
- Write any more functional specs needed before coding.
- Agree on a taxonomy for the hierarchy of learning targets.
- Agree on an overall approach to identifying the kinds of relationships between different pieces of knowledge?
- [(done)](https://github.com/openlearningtools/opencompetencies/blob/master/GLOSSARY.md) Write a glossary for the first few levels in the taxonomy
- Move much of this file to a wiki. Readme is mostly technical, and links to the wiki.
- Agree on which framework to use

[top](#top)
