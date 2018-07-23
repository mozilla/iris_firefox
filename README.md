# iris
Visual Test Suite for Firefox

* Supports Mac, Windows and Ubuntu Linux.
* For step-by-step setup instructions, please see our [wiki](https://github.com/mozilla/iris/wiki/Setup).

* Declare platform specific [dependencies](http://setuptools.readthedocs.io/en/latest/setuptools.html#declaring-platform-specific-dependencies)

To run these tests you will need [Python 2][] and [pipenv][] installed. Once
you have these, run the following:

```
$ pipenv install
$ pipenv run iris
```

For additional full command line options run `pipenv run iris --help`.

[Python 2]: http://docs.python-guide.org/en/latest/starting/installation/#legacy-python-2-installation-guides
[pipenv]: http://docs.python-guide.org/en/latest/dev/virtualenvs/#installing-pipenv
