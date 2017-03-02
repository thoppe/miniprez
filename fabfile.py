from fabric.api import local
import time
import shutil
import os

f_tutorial = "tutorial.md"

def build():
    local("python miniprez {}".format(f_tutorial))

def watch():
    while True:
        build()
        time.sleep(1.0)

def test():
    local("nosetests -vs")
    local("flake8 --ignore=E501,F821 miniprez tests")
    local("aspell check README.md")
    local("check-manifest")
    local("python miniprez tutorial.md")

def pep():
    local("autopep8 miniprez/*.py tests/*.py -a --in-place --jobs=0")

def coverage():
    local("nosetests --with-coverage --cover-package=miniprez")

def clean():
    if os.path.exists("static"):
        shutil.rmtree("static")
    if os.path.exists("tutorial.html"):
        os.remove("tutorial.html")
    


