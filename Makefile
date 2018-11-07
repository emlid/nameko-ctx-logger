init:
	git submodule update --init --recursive
	pip install pipenv==2018.6.25
	pipenv install --dev

style-check:
	pipenv run flake8 --config code-quality/python/flake8

lint:
	pipenv run pylint --rcfile code-quality/python/pylintrc \
					  nameko_worker_logger

install:
	pipenv run pip install -e .