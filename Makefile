target = tutorial
target = test

all:
	python miniprez/miniprez.py $(target).md

clean:
	rm -vf *~ $(target).html
	find . -name "*.pyc" | xargs -I {} rm -v {}
	find . -name "*~" | xargs -I {} rm -v {}

edit:
	emacs $(target).md &

view:
	xdg-open $(target).html &

build:
	watch -n 1 make

watch:
	make build

commit:
	git commit -a
	git push
