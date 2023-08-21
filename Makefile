install:
	poetry install

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user --force-reinstall dist/*.whl

lint:
	poetry run flake8 page_loader
	poetry run flake8 tests

test:
	poetry run pytest --cov=page_loader --cov-report xml
	poetry run pytest -vv

selfcheck:
	poetry check

check: selfcheck test lint

.PHONY: install test lint selfcheck check build
