import io
import json
import pytest

from app.resume import Resume


def test_resume_file_is_valid():
    json_resume = Resume()
    assert json_resume.validate()


def test_resume_file_can_fail():
    fake_resume_data = json.dumps({"fake_resume": "blahblah"})
    fake_resume_file = io.StringIO(fake_resume_data)
    with pytest.raises(TypeError):
        Resume(fake_resume_file)
    fake_resume_file.close()


def test_resume_fields_can_be_accessed():
    test = Resume()
    test.basics.name
    test.basics.location
    [job.company for job in test.work]
    [skill.keywords for skill in test.skills]
