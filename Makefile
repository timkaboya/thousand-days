database:
	psql postgres postgres -f	etc/dbsetup.sql

test:
	./manage.py shell < etc/testant.py
