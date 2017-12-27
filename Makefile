.PHONY: test run

test:
	PYTHONPATH=./lib python tests/runner.py /tmp/google-cloud-sdk/

run:
	dev_appserver.py ./app.yaml --host=0.0.0.0 --admin_host=0.0.0.0 --log_level=debug

init:
	pip2 install -t lib/ -r requirements.txt -U
