import errno
import filecmp
import os
import pytest

from resume_generator.general.job_description import JobDescription

MOCK_JOB_SITE = "./tests/mocks/job_site.html"
MOCK_APPLICATION_NAME = "pytest-mock"
MOCK_APPLICATION_FOLDER = f"./job_applications/{MOCK_APPLICATION_NAME}"
MOCK_RECORD_SITE_CONTENT = f"{MOCK_APPLICATION_FOLDER}/site_content.html"
MOCK_RECORD_BULLET_POINTS = f"{MOCK_APPLICATION_FOLDER}/bullet_points.json"

SNAPSHOT_SITE_CONTENT = "./tests/snapshots/site_content.html"
SNAPSHOT_BULLET_POINTS = "./tests/snapshots/bullet_points.json"


@pytest.fixture(scope="module")
def job():
    job = JobDescription(
        application_name=MOCK_APPLICATION_NAME, html_file=MOCK_JOB_SITE
    )
    yield job
    os.remove(MOCK_RECORD_SITE_CONTENT)
    os.remove(MOCK_RECORD_BULLET_POINTS)
    os.rmdir(MOCK_APPLICATION_FOLDER)


def test_mock_job_description_records_properly(job):
    # Clean up existing files
    silent_remove(job.get_site_content_filename())
    silent_remove(job.get_bullet_points_filename())

    job.record()

    # Check that it matches the expected snapshot
    assert filecmp.cmp(MOCK_RECORD_SITE_CONTENT, SNAPSHOT_SITE_CONTENT)
    assert filecmp.cmp(MOCK_RECORD_BULLET_POINTS, SNAPSHOT_BULLET_POINTS)


def silent_remove(filename):
    try:
        os.remove(filename)
    except OSError as e:
        # if not error for "no such file or directory"
        if e.errno != errno.ENOENT:
            raise
