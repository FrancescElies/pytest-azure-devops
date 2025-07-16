# creates venv
init:
		uv venv
		uv pip install -e .
		uv tool install tox --with tox-uv
# runs black
format:
		uv pip install black
		black .
# makes .tar.gz and .whl
build:
		uv build
# to pypi
publish:
		uv publish
# runs tox
test:
		tox -p
# runs ruff
lint:
		uv pip install ruff
		ruff check
