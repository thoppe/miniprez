target = test

all:
	python minprez/minprez.py $(target).md

clean:
	rm -vf *~ $(target).html *.pyc

edit:
	emacs $(target).md &

view:
	xdg-open $(target).html &

build:
	watch -n 1 make

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
# Build dependencies
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=

build_deps:
	-git submodule add https://github.com/jlantunez/webslides
	git submodule update --init
	cd webslides && git pull origin master && cd ..
	git submodule status
