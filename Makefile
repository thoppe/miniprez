target = tutorial
target = test

all:
	python miniprez/miniprez.py $(target).md

clean:
	rm -vf *~ $(target).html *.pyc

edit:
	emacs $(target).md &

view:
	xdg-open $(target).html &

build:
	watch -n 1 make

watch:
	make build
