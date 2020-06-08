best_resume_ever_path=$(shell python -c "import config; print(config.BEST_RESUME_EVER_PATH)")
output_yaml=$(shell python -c "import config; print(config.OUTPUT_YAML)")


help:
	@echo "make init"
	@echo "	Setup venv and install packages"
	@echo ""
	@echo "make init_encoder"
	@echo "	First time setup for universal-sentence-encoder. Takes about 5-10 mins."
	@echo ""
	@echo "make application name=NAME url=URL"
	@echo "	Create an job_applications/NAME/ folder with files for a job applications."
	@echo "	URL: should be for the job description page."
	@echo "	NAME: Is just a user defined name for organizing."
	@echo ""
	@echo "make redo_application name=NAME"
	@echo "	Rebuild an application based on the copy of the data when it was first run."
	@echo "	This is useful for debugging or precise edits"
	@echo "	NAME: Is just a user defined name for organizing."
	@echo ""
	@echo "make pdf"
	@echo "	Create a pdf resume based on best-resume-ever work."
	@echo "	It gets the PATH to the best-resume-ever repo from config.py."
	@echo ""
	@echo "make tests"
	@echo "	Run test suite. Skipping the 'slow' end-to-end tests"
	@echo ""
	@echo "make tests_full"
	@echo "	Run full test suite. Including end-to-end test."


init:
	@echo "\n[make] Create venv"
	python -m virtualenv venv --python python3
	@echo "\n[make] Install pip-tools to venv"
	venv/bin/pip install pip-tools
	@echo "\n[make] Compile requirements.in to requirements.txt"
	venv/bin/python -m piptools compile
	@echo "\n[make] Install requirements.txt to venv"
	venv/bin/pip install -r requirements.txt


init_encoder:
	@echo "\n[make] Create folder to store local universal-sentence-encoder"
	mkdir -p library/universal-sentence-encoder
	@echo "\n[make] CURL the tarball and extract its contents"
	cd library/universal-sentence-encoder; curl -L "https://tfhub.dev/google/universal-sentence-encoder/4?tf-hub-format=compressed" | tar -zxvC .


application:
	@echo "\n$(date)" >> job_applications/${name}/application.log
	@echo "\n[make] Creating Job Application for ${name}"
	mkdir -p job_applications/${name}/
	@echo "mkdir -p job_applications/${name}/" >> job_applications/${name}/application.log
	@echo "\n[make] Get job bullets and raw HTML from ${url}"
	venv/bin/python -m resume_generator get_job_bullets --application_name ${name} --url ${url} 
	@echo "venv/bin/python -m resume_generator get_job_bullets --application_name ${name} --url ${url}" >> job_applications/${name}/application.log
	@echo "\n[make] Writing special resume.json based on job description"
	venv/bin/python -m resume_generator build_resume_json --application_name ${name}
	@echo "venv/bin/python -m resume_generator build_resume_json --application_name ${name}" >> job_applications/${name}/application.log
	@echo "\n[make] Make PDF from resume.json"
	make pdf name=${name}
	@echo "make pdf name=${name}" >> job_applications/${name}/application.log
	@echo "\n[make] All done with application to ${name}.\n"


redo_application:
	@echo "\n[make] Get job bullets from local copy of HTML page"
	venv/bin/python -m resume_generator get_job_bullets --application_name ${name} --rebuild
	@echo "\n[make] Writing special resume.json based on job description; from the local copy of resume.json"
	venv/bin/python -m resume_generator build_resume_json --application_name ${name} --rebuild
	@echo "\n[make] Make PDF from resume.json"
	make pdf name=${name}
    

pdf:
	@echo "\n[make] Convert resume_json to yaml_resume.yml"
	venv/bin/python -m resume_generator build_resume_yaml --application_name ${name}
	@echo "\n[make] Overwrite best-resume-ever data.yml with newly created one"
	cp ${output_yaml} ${best_resume_ever_path}/resume/data.yml
	@echo "\n[make] Use best-resume-ever to create PDF resume. Wait 15 secs...."
	@cd ${best_resume_ever_path}; npm run export
	@echo "\n[make] Move pdf export to application folder"
	mv ${best_resume_ever_path}/pdf/eric-jalbert.pdf ./job_applications/${name}/eric_jalbert_${name}.pdf
	@echo "\n[make] Move yaml_resume.yml to application folder ${name}"
	mv ${output_yaml} ./job_applications/${name}/yaml_resume.yml
	@echo "\n[make] Cleanup best-resume-ever repo"
	rm -r ${best_resume_ever_path}/pdf

tests:
	venv/bin/python -m pytest tests -k "not slow"

tests_full:
	venv/bin/python -m pytest tests -rP


.PHONY: help variables init init_encoder application redo_application pdf tests tests_full
