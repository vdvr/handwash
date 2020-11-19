# Setup
Clone this repository, eg: `git clone https://github.com/vdvr/handwash`.

## Python - aka UI - setup
Make sure you have python version 3.8 installed, check with `python -V` or
`python3 -V`. Note that when you use the command python3 you also need to use
pip3 (and not pip).

## Install and use pipenv
``` bash
pip3 install pipenv
pipenv install --dev
pipenv shell
```

# Developer notes
To add python dependencies use `pipenv install <pypi package>`.
