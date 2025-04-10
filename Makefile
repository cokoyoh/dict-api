# Makefile

run:
	cd src/ && uvicorn main:app --host 0.0.0.0 --port 8000

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

install:
	pip install -r requirements.txt
