import json
import pytest

from resume_generator.general.job_description import JobDescription

MOCK_APPLICATION_NAME = "pytest-mock"

MOCK = "./tests/mocks/job_site"
SNAPSHOT = "./tests/snapshots/bullet_points"

MOCK_JOB_SITE_NORMAL = f"{MOCK}.html"
SNAPSHOT_BULLET_POINTS_NORMAL = f"{SNAPSHOT}.json"
MOCK_JOB_SITE_WITH_HEADER_LI = f"{MOCK}_with_header_li.html"
SNAPSHOT_BULLET_POINTS_WITH_HEADER_LI = f"{SNAPSHOT}_with_header_li.json"
MOCK_JOB_SITE_WITH_COMPENSATION = f"{MOCK}_with_compensation.html"
SNAPSHOT_BULLET_POINTS_WITH_COMPENSATION = f"{SNAPSHOT}_with_compensation.json"
MOCK_JOB_SITE_WITH_WHAT_WE_OFFER = f"{MOCK}_with_what_we_offer.html"
SNAPSHOT_BULLET_POINTS_WITH_WHAT_WE_OFFER = f"{SNAPSHOT}_with_what_we_offer.json"


@pytest.fixture(scope="module")
def normal_site():
    job = JobDescription(
        application_name=MOCK_APPLICATION_NAME, html_file=MOCK_JOB_SITE_NORMAL
    )
    yield job


@pytest.fixture(scope="module")
def with_header_li_site():
    job = JobDescription(
        application_name=MOCK_APPLICATION_NAME, html_file=MOCK_JOB_SITE_WITH_HEADER_LI
    )
    yield job


@pytest.mark.parametrize(
    "mock_html_file, bullet_points_file",
    [
        pytest.param(MOCK_JOB_SITE_NORMAL, SNAPSHOT_BULLET_POINTS_NORMAL, id="normal"),
        pytest.param(
            MOCK_JOB_SITE_WITH_HEADER_LI,
            SNAPSHOT_BULLET_POINTS_WITH_HEADER_LI,
            id="with_header_li",
        ),
        pytest.param(
            MOCK_JOB_SITE_WITH_COMPENSATION,
            SNAPSHOT_BULLET_POINTS_WITH_COMPENSATION,
            id="with_compensation",
        ),
        pytest.param(
            MOCK_JOB_SITE_WITH_WHAT_WE_OFFER,
            SNAPSHOT_BULLET_POINTS_WITH_WHAT_WE_OFFER,
            id="with_what_we_offer",
        ),
    ],
)
def test_bullet_points_match_snapshot(mock_html_file, bullet_points_file):
    job = JobDescription(
        application_name=MOCK_APPLICATION_NAME, html_file=mock_html_file
    )
    bullet_points = job.get_bullet_points()

    with open(bullet_points_file) as f:
        snapshot = json.load(f)

    assert bullet_points == snapshot
