from dataclasses import dataclass
from typing import List


@dataclass
class Profile:
    """Class to model professional profiles like github, linkedin"""

    network: str
    username: str
    url: str


@dataclass
class Location:
    """Models location information into easy format"""

    city: str
    countryCode: str
    region: str

    def __str__(self):
        return f"{self.city}, {self.region}, {self.countryCode}"


@dataclass
class Basics:
    """Class to model basic personal information from the resume"""

    name: str
    label: str
    email: str
    phone: str
    website: str
    summary: str
    location: Location
    profiles: List[Profile]


@dataclass
class Work:
    """Model work experiences and highlights"""

    company: str
    position: str
    website: str
    startDate: str
    endDate: str
    summary: str
    highlights: List[str]


@dataclass
class Education:
    """Model Academic experiences and highlights"""

    institution: str
    area: str
    studyType: str
    startDate: str
    endDate: str
    thesis: str = None
    publications: str = None


@dataclass
class Skills:
    """Model skill highlights"""

    name: str
    keywords: List[str]
