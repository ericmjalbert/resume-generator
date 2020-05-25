help:
	@echo "init: 		Setup venv and install packages"
	@echo "init_pdf:	Setup npm install for the best-resume-ever export"
	@echo "pdf: 		Create a pdf resume based on best-resume-ever work"
	@echo "tests: 		Run test suite to make sure development changes don't break things"

init:
	@echo "\n[make] Create venv"
	python -m virtualenv venv --python python3
	@echo "\n[make] Install pip-tools to venv"
	venv/bin/pip install pip-tools
	@echo "\n[make] Compile requirements.in to requirements.txt"
	venv/bin/python -m piptools compile
	@echo "\n[make] Install requirements.txt to venv"
	venv/bin/pip install -r requirements.txt

pdf:
	@echo "\n[make] Convert resume_json to yaml_resume.yml"
	venv/bin/python main.py
	@echo "\n[make] Overwrite best-resume-ever data.yml with newly created one"
	mv ./yaml_resume.yml ${BEST_RESUME_EVER_ABS_PATH}/resume/data.yml
	@echo "\n[make] Use best-resume-ever to create PDF resume"
	cd ${BEST_RESUME_EVER_ABS_PATH}; npm run export
	@echo "\n[make] Move pdf export to this repo"
	mv ${BEST_RESUME_EVER_ABS_PATH}/pdf/eric-jalbert.pdf ./resume_eric_jalbert.pdf
	@echo "\n[make] Cleanup best-resume-ever repo"
	rm -r ${BEST_RESUME_EVER_ABS_PATH}/pdf

tests:
	venv/bin/python -m pytest tests


.PHONY: help init pdf tests
