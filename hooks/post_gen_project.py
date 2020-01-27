import os

packages = [
    'black',
    'pip',
    'setuptools',
]

pip_only_packages = [
]

{% if 's3' in cookiecutter.dataset_storage %}
packages += ['awscli']
{% endif %}

dependencies = '{{ cookiecutter.dependency_file }}'

def write_dependencies():
    if dependencies == 'requirements.txt':
        with open(dependencies, 'w') as f:
            lines = sorted(packages + pip_only_packages)

            lines += [
                ""
                "-e ."
            ]

            f.write("\n".join(lines))

    elif dependencies == 'environment.yml':
        with open(dependencies, 'w') as f:
            lines = ["name: {{ cookiecutter.repo_name }}",
                     "dependencies:"]

            lines += [f"  - {p}" for p in packages]

            lines += ["  - pip:"] + [f"    - {p}" for p in pip_only_packages]

            lines += ['    - -e .']

            lines += ["  - python={{ cookiecutter.python_version_number }}"]

            f.write("\n".join(lines))


    elif dependencies == 'Pipfile':
        with open(dependencies, 'w') as f:
            lines = ["[packages]"]
            lines += [f'{p} = "*"' for p in sorted(packages + pip_only_packages)]

            lines += ['"{{ cookiecutter.module_name }}" = {editable = true, path = "."}']

            lines += [
                "",
                "[requires]",
                'python_version = "{{ cookiecutter.python_version_number }}"'
            ]

            f.write("\n".join(lines))


write_dependencies()
