
test: rapid1000.pdf
	open -a preview rapid1000.pdf

rapid1000.html: rapid1000.haml list.txt rapidmag.rb
	env STATIC_DIR=../thoustatics ruby rapidmag.rb rapid1000.haml list.txt > rapid1000.html
	env STATIC_DIR=../static ruby rapidmag.rb rapid1000.haml list.txt > ../thoutemplates/rapid1000.html

../thoustatics/stylesheets/rapid1000.css: ../thoustatics/stylesheets/rapid1000.scss
	sass --update ../thoustatics/stylesheets/rapid1000.scss

rapid1000.pdf: rapid1000.html ../thoustatics/stylesheets/rapid1000.css
	prince -o rapid1000.pdf rapid1000.html

clean:
	rm -f rapid1000.pdf rapid1000.html ../thoustatics/stylesheets/rapid1000.css
