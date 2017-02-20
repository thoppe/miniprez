from fabric.api import local

def test():
    local("nosetests -vs")
    #local("flake8 miniprez tests")
    #local("aspell check README.md")
    #local("detox")

def cleanup():
    #local("autopep8 miniprez/*.py tests/*.py --in-place")
    local("autopep8 miniprez/*.py -a --in-place")

