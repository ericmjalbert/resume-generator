import argparse
import json
import pathlib
import time

from selenium import webdriver
from bs4 import BeautifulSoup

from config import JOB_APP_FOLDER_TEMPLATE


class JobDescription:
    def __init__(self, application_name, url=None, html_file=None):
        """Runs through the scraping of the given job description site.

        html_file is only used for pytest
        url is only for production usage
        """
        self.application_name = application_name
        self.url = url
        self.html_file = html_file

        self.folder = JOB_APP_FOLDER_TEMPLATE.format(
            application_name=self.application_name
        )
        self.site_content = self.get_site_content()
        self.bullet_points = self.get_bullet_points()

    def get_site_content(self):
        if self.url:
            site_content = self.get_url_content()
        if self.html_file:
            site_content = self.get_html_file_content()
        return site_content

    def get_url_content(self):
        """Use Selenium to open website with Javascript support and grab HTML."""
        driver = webdriver.Chrome()
        driver.get(self.url)
        time.sleep(5)
        site_content = BeautifulSoup(driver.page_source, "html.parser")
        driver.close()
        return site_content

    def get_html_file_content(self):
        """Load local HTML file to grab site content."""
        with open(self.html_file) as f:
            soup = BeautifulSoup(f, "html.parser")
        return soup

    def get_bullet_points(self):
        bullet_points = [
            li.text
            for li in self.site_content.find_all("li")
            if self.is_valid_job_requirement(li) and not self.is_company_benefits(li)
        ]

        return bullet_points

    @staticmethod
    def is_company_benefits(li):
        """If any of the special words are in the text than flag it as a benefit."""
        company_benefit_word_list = [
            "we offer",
            "salary",
            "retirement",
            "vacation",
            "weeks",
            "laptop",
            "benefits",
            "healthcare",
            "company retreat",
            "annual",
            "groceries",
            "great place to work",
            "coffee",
            "catered",
            "ping pong",
        ]
        if any(word in li.text.lower() for word in company_benefit_word_list):
            return True
        return False

    @staticmethod
    def is_valid_job_requirement(li):
        """Removes li points that are nonsense or not job requirements."""
        if (
            len(li.text.split()) > 4
            and "\n" not in li.text
            and not li.findChildren("a")
        ):
            return True
        return False

    def get_site_content_filename(self):
        return f"{self.folder}/site_content.html"

    def get_bullet_points_filename(self):
        return f"{self.folder}/bullet_points.json"

    def record(self):
        print(f"Ensuring {self.folder} exists")
        pathlib.Path(f"{self.folder}").mkdir(parents=True, exist_ok=True)

        filename = self.get_site_content_filename()
        print(f"Recording {self.application_name} {filename}")
        with open(filename, "w") as f:
            f.write(str(self.site_content))

        filename = self.get_bullet_points_filename()
        print(f"Recording {self.application_name} {filename}")
        with open(filename, "w") as f:
            json.dump(self.bullet_points, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url")
    parser.add_argument("--application_name")
    args = parser.parse_args()

    job = JobDescription(args.application_name, args.url)
    job.record()
