venv:
	python3 -m venv .venv

install:
	. .venv/bin/activate && pip install -r requirements.txt

run:
	. .venv/bin/activate && python apps/simple-label-printer/print_label.py

lint:
	. .venv/bin/activate && ruff check .

format:
	. .venv/bin/activate && black .

test:
	. .venv/bin/activate && pytest