# Code Atlas

Code Atlas was created in spite of wasting so much time searching for trivial things I knew I had done before. I often found myself looking through previous projects or tracking down articles for that code snippet I knew existed.  I thought there had to be a better way to do things. So I created Code Atlas.

Code Atlas lets users create "Notes". Notes can store markdown, support code highlighting, tagging as well as url references. These notes can be searched by their tags, a query or both. Public notes can be cloned.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Installing

You will need to create database. This may require changes needing to be made to the settings file: `codeatlas/settings/local.py`

```
git clone https://github.com/Maxamuss/code-atlas
python -m venv env
./env/Scripts/activate
pip install -r requirments/local.txt
python manage.py migrate
python manage.py runserver
```

Then visit `http://127.0.0.1/` in your browser to view the site

## Running the tests

To run tests:

```
python manage.py test
```

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used
* [Django Rest Framework](https://www.django-rest-framework.org/) - Rest frameword used

## Contributing

Please feel free to contribute.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/Maxamuss/code-atlas/tags). 

## Authors

* **Max Wilkinson**

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## Acknowledgments

* Big shout out to [r/django](https://www.reddit.com/r/django) 
