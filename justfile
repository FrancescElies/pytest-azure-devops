init:
		uv venv
		uv tool install tox --with tox-uv
build:
		uv build
publish:
		uv publish
test:
		tox -p
