import filecmp
import os

import pytest

from resume_generator.general.resume import Resume
from resume_generator.pdf.json_to_yaml import convert_to_yaml

MOCK_RESUME_FILE = "./tests/mocks/resume.json"
MOCK_YAML_OUTPUT = "./tests/mocks/resume.yml"

SNAPSHOT_YAML_OUTPUT = "./tests/snapshots/resume.yml"


def test_mock_resume_file_is_valid():
    json_resume = Resume(MOCK_RESUME_FILE)
    assert json_resume.validate()


def test_mock_resume_converts_to_yaml(resume_yaml):
    # Check that yaml exists
    assert os.path.isfile(resume_yaml)

    # Check that it matches the expected snapshot
    print(resume_yaml, SNAPSHOT_YAML_OUTPUT)
    assert filecmp.cmp(resume_yaml, SNAPSHOT_YAML_OUTPUT)


@pytest.fixture(scope="module")
def resume_yaml():
    convert_to_yaml(resume_file=MOCK_RESUME_FILE, output_yaml=MOCK_YAML_OUTPUT)
    yield MOCK_YAML_OUTPUT
    os.remove(MOCK_YAML_OUTPUT)
