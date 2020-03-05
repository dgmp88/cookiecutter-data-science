
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

{% if cookiecutter.environment_manager == 'conda' %}
conda-import:
	conda env create -f environment.yml

conda-export:
		conda env export --no-builds > environment.yml
{% endif %}

