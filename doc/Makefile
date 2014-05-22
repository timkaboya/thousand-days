test: rapid1000.pdf
	open -a preview rapid1000.pdf

rapid1000.html: rapid1000.haml
	ruby rapidmag.rb rapid1000.haml list.txt > rapid1000.html

rapid1000.css: rapid1000.scss
	sass --update rapid1000.scss

rapid1000.pdf: rapid1000.html rapid1000.css
	prince -o rapid1000.pdf rapid1000.html

clean:
	rm -f rapid1000.pdf rapid1000.html rapid1000.css
