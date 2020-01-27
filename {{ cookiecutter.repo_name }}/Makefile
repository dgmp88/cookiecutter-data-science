.PHONY: clean data lint requirements sync_data_down sync_data_up

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = {{ cookiecutter.repo_name }}
PYTHON_INTERPRETER = python{{ cookiecutter.python_version_number }}


#################################################################################
# COMMANDS                                                                      #
#################################################################################


## Make Dataset
data: requirements
	$(PYTHON_INTERPRETER) {{ cookiecutter.module_name }}/data/make_dataset.py

# Install the package locally so we can use it in notebooks etc
install-package:
	# This does a local install so updates are recognised on the fly
	pip install -e ./

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8
lint:
	flake8 {{ cookiecutter.module_name }}

## Format using black
format:
	black {{ cookiecutter.module_name }}

{% if 's3' in cookiecutter.dataset_storage %}
## Download Data from storage system
sync_data_down:
	{% if "s3" in cookiecutter.dataset_storage %}
	aws s3 sync s3://{{ cookiecutter.dataset_storage.s3.bucket }}/data/\
		data/ {% if cookiecutter.dataset_storage.s3.aws_profile != 'default' %} --profile {{ cookiecutter.dataset_storage.s3.aws_profile }}{% endif %}
	{% elif cookiecutter.dataset_storage.azure %}
	az storage blob download-batch -s {{ cookiecutter.dataset_storage.azure.container }}/data/ \
		-d data/
	{% elif cookiecutter.dataset_storage.gcs %}
	gsutil cp {{ cookiecutter.dataset_storage.gcs.bucket }}/data/ data/
	{% endif %}

## Upload Data to storage system
sync_data_up:
	{% if "s3" in cookiecutter.dataset_storage %}
	aws s3 sync s3://{{ cookiecutter.dataset_storage.s3.bucket }}/data/ data/\
		{% if cookiecutter.dataset_storage.s3.aws_profile %} --profile $(PROFILE){% endif %}
	{% elif cookiecutter.dataset_storage.azure %}
	az storage blob upload-batch -d {{ cookiecutter.dataset_storage.azure.container }}/data/ \
		-s data/
	{% elif cookiecutter.dataset_storage.gcs %}
	gsutil cp data/ {{ cookiecutter.dataset_storage.gcs.bucket }}/data/
	{% endif %}
{% endif %}

{% if cookiecutter.environment_manager != 'none' %}
## Set up python interpreter environment
create-environment:
	{% if cookiecutter.environment_manager == 'conda' %}
	conda env create --name $(PROJECT_NAME) python={{ cookiecutter.python_version_number }}{% if cookiecutter.dependency_file == 'environment.yml' %} -f environment.yml{% endif %}
	@echo ">>> conda env created. Activate with:\nconda activate $(PROJECT_NAME)"
	{% elif cookiecutter.environment_manager == 'virtualenv' %}
	@bash -c "source `which virtualenvwrapper.sh`;mkvirtualenv $(PROJECT_NAME) --python=$(PYTHON_INTERPRETER)"
	@echo ">>> New virtualenv created. Activate with:\nworkon $(PROJECT_NAME)"
	{% elif cookiecutter.environment_manager == 'pipenv' %}
	pipenv install
	@echo ">>> New pipenv created. Activate with:\npipenv shell"
	{% endif %}
{% endif %}

{% if cookiecutter.environment_manager == 'conda' %}
export-environment:
	conda env export > environment.yml
{% endif %}

