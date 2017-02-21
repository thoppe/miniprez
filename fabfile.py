from fabric.api import local

def test():
    local("nosetests -vs")
    local("flake8 --ignore=E501 miniprez tests")
    local("aspell check README.md")
    #local("detox")

def pep():
    local("autopep8 miniprez/*.py tests/*.py -a --in-place --jobs=0")

