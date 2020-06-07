""" End-to-end test for creating the custom resume.

This ensures that the `make application` command will work up until the `make
pdf` part. Mainly to make sure we have a quick way to always test that the
full setup works and doesn't result in an empty resume.

"""

import filecmp
import json
import os
import shutil

import pytest

from resume_generator.general.application import Application
from resume_generator.pdf.json_to_yaml import convert_to_yaml
from resume_generator.general.job_description import JobDescription

MOCK_JOB_SITE = "./tests/mocks/job_site.html"
MOCK_RESUME_FILE = "./tests/mocks/resume.json"
MOCK_APPLICATION_NAME = "pytest-end-to-end"
MOCK_APPLICATION_FOLDER = f"./job_applications/{MOCK_APPLICATION_NAME}"


@pytest.fixture(scope="module", autouse=True)
def mock_application_folder():

    # Create and record mock job description
    job = JobDescription(
        application_name=MOCK_APPLICATION_NAME, html_file=MOCK_JOB_SITE
    )
    job.record()

    # Create and record mock application
    application = Application(
        application_name=MOCK_APPLICATION_NAME, resume_file=MOCK_RESUME_FILE
    )
    application.record()

    # Convert mock application to yaml
    convert_to_yaml(
        f"{MOCK_APPLICATION_FOLDER}/application_resume.json",
        f"{MOCK_APPLICATION_FOLDER}/yaml_resume.yml",
    )

    # Now do tests on this folder
    yield MOCK_APPLICATION_FOLDER

    # Delete the whole folder
    shutil.rmtree(MOCK_APPLICATION_FOLDER)


@pytest.fixture(scope="module")
def original_resume_filename(mock_application_folder):
    return f"{mock_application_folder}/original_resume.json"


@pytest.fixture(scope="module")
def application_resume_filename(mock_application_folder):
    return f"{mock_application_folder}/application_resume.json"


def test_job_application_files_exist__slow(
    mock_application_folder, original_resume_filename, application_resume_filename
):
    # assert that all the "application record" files exist
    assert os.path.isfile(f"{mock_application_folder}/bullet_points.json")
    assert os.path.isfile(f"{mock_application_folder}/site_content.html")
    assert os.path.isfile(f"{mock_application_folder}/yaml_resume.yml")
    assert os.path.isfile(original_resume_filename)
    assert os.path.isfile(application_resume_filename)


def test_application_resume_is_different__slow(
    original_resume_filename, application_resume_filename
):
    assert filecmp.cmp(original_resume_filename, application_resume_filename) is False


def test_application_resume_has_correct_highlight_counts__slow(
    application_resume_filename, mock_application_folder
):
    with open(application_resume_filename) as f:
        application_resume_json = json.load(f)

    # Mock Resume should have exactly 4 here
    first_work_highlights = application_resume_json["work"][0]["highlights"]
    assert len(first_work_highlights) == 4

    # Mock Resume should have exactly 3 here
    first_skills_highlights = application_resume_json["skills"][0]["keywords"]
    assert len(first_skills_highlights) == 3
