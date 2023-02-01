# Breddit

## Overview
A reddit like website design that allows users to submit posts, edit them, up-vote and down-vote other posts, search by name, vote score and date added. Every post has its own page where users can discuss on the given subject in the comment section. The website also features a Front page where only posts of the followed users are displayed.

## Specification
This project contains the following features:

* **Models**: the application has three models in addition to the `User` model: one for posts, one for comments, and one for user following logic.
* **All page (landing page)**: Users are able to see 10 newest posts (by default) and can choose to sort them by vote score, and date submitted. Every post contains the title which leads to the separate post page, post description, arrows for voting, current voting score, username of the creator which leads to his profile, edit button if the logged-in user is the creator of the post and date the post was submitted.
* **Front page**: Only available to logged-in users, while non-logged-in users will be redirected to the login page. Front page contains only the posts from users that the logged-in user follows while post contains the same information like in the landing page.
* **New post**: Leads to a new page that allows logged-in users to enter the title and text of their post and submit it to the site.
* **Search bar**: Lets users search posts whose title contains entered keywords.
* **Post Page**: Clicking on a post takes users to a page specific to that post. On that page, users are able to view all details about the post, including the submitted comments.
  * If the user is signed in, the user is able to add the comment to post and also reply to other comments.
  * If the user is signed in, and the user is the creator of the post user is able to edit the post.
  * If the user is signed in, the user is able to vote/change a given vote on the post.
* **Django Admin Interface**: Via the Django admin interface, a site administrator is able to view, add, edit, and delete any posts, comments, and user following made on the site.

## Setup
Requires Python3 and the package installer for Python (pip) to run:

* Install requirements (Django4): `pip install -r requirements.txt`
* After cloning the repository, refer to the project folder and:
  1. Create new migrations based on the changes in models: `python3 manage.py makemigrations`
  2. Apply the migrations to the database: `python3 manage.py migrate`
  3. Create a superuser to be able to use Django Admin Interface: `python3 manage.py createsuperuser`
  4. Run the app locally: `python3 manage.py runserver 8000` (or your desired port instead of default 8000)
  5. Visit the site: `http://localhost:8000` 
  6. Enjoy!

## Topics
Built with [`Python`](https://www.python.org/downloads/), [`Django`](https://www.djangoproject.com/),HTML/CSS and ['Crispy'](https://django-crispy-forms.readthedocs.io/en/latest/).

## To do:
Some challenges I would make in my free time:
* Add a subreddit feature
* Make a nicer front-end design.
