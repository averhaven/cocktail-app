setup:
	python3 -m venv venv
	venv/bin/pip install -r requirements.txt

run:
	venv/bin/uvicorn cocktail_api.main:app --reload

test:
	venv/bin/pytest

dbdata:
	PYTHONPATH=. venv/bin/python3 scripts/loading_cocktails_into_db.py