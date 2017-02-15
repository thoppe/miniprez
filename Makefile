target = tutorial
#target = test

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

watch:
	python miniprez/miniprez.py $(target).md --watch=1

commit:
	git commit -a
	git push
