# Makefile
venv:
	python3 -m venv .venv

run:
	cd src && uvicorn main:app --host 0.0.0.0 --port 8000

run-dev:
	make run -- --reload

run-prod:
	make run -- --workers 4

test:
	pytest -s -v 

test-watch:
	ptw

format:
	black .

requirements:
	pip freeze > requirements.txt

install:
	pip install -r requirements.txt
