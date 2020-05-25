import json

from dacite import from_dict
from app.model import Basics, Education, Skills, Work
from config import RESUME_FILE


def read_json_file(filename):
    with open(filename) as f:
        resume_json = json.load(f)
    return resume_json


class Resume:
    def __init__(self, resume_file=RESUME_FILE):
        self.resume_file = resume_file
        self.resume_json = read_json_file(resume_file)

        self.basics = self.parse_resume_for_field(model=Basics, field="basics")
        self.education = self.parse_resume_for_field(model=Education, field="education")
        self.skills = self.parse_resume_for_field(model=Skills, field="skills")
        self.work = self.parse_resume_for_field(model=Work, field="work")

    def parse_resume_for_field(self, model, field):
        """Uses the models Dataclass to create the class object from the given JSON.

        This is the default behaviour of `dacite.from_dict`, but it doesn't
        handle iterating through a list of dicts. This function is created to
        handle those cases.
        """
        resume_object = self.resume_json.get(field)
        if isinstance(resume_object, dict):
            parsed = from_dict(data_class=model, data=resume_object)
        elif isinstance(resume_object, list):
            parsed = [from_dict(data_class=model, data=item) for item in resume_object]
        else:
            raise TypeError(
                "Bad Resume File; basics, work, skills, education must be Lists or Dict"
            )
        return parsed

    def field_exists(self, field_path):
        json = self.resume_json
        try:
            for field in field_path.split("."):
                json = json[field]
            return True
        except KeyError:
            return False

    def validate(self):
        """Validates that the needed fields exist in the master resume_json file ONLY.

        This doesn't actually do any check that the dataclass in model.py exists.
        Thus we need to make sure that models match this needed_fields list.
        """
        NEEDED_FIELDS = [
            "basics.name",
            "basics.label",
            "basics.email",
            "basics.phone",
            "basics.website",
            "basics.summary",
            "basics.location.city",
            "basics.location.countryCode",
            "basics.location.region",
            "work",
            "education",
            "skills",
            # TODO figure out how to handle lists in this: "basics.profiles.url",
        ]
        return all([self.field_exists(field) for field in NEEDED_FIELDS])
