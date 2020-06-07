import argparse
import json

from resume_generator.general.resume import Resume
from resume_generator.general.resume_highlights import ResumeHighlights
from config import JOB_APP_FOLDER_TEMPLATE, RESUME_FILE


class Application:
    def __init__(self, application_name, resume_file=RESUME_FILE, rebuild=False):
        self.application_name = application_name
        self.folder = JOB_APP_FOLDER_TEMPLATE.format(application_name=application_name)
        if not rebuild:
            self.resume_file = resume_file
        else:
            self.resume_file = f"{self.folder}/original_resume.json"
        self.job_bullets = self._get_job_bullets()
        self.master_resume = Resume(self.resume_file)

    def record(self):
        """Writes the needed files to local disk.

        This writes the original resume since we need it whenever we do re-runs.
        This also writes the new custom "application resume" since that's the
        one that will be used for the PDF generation.
        """
        self.record_master_resume()
        self.record_application_resume()

    def record_master_resume(self):
        with open(f"{self.folder}/original_resume.json", "w") as f:
            json.dump(self.master_resume.resume_json, f)

    def record_application_resume(self):
        # Make a new instance of it since we're updating values
        resume = Resume(self.resume_file)
        new_work_resume = self._calculate_top_work_highlights()
        new_skills_resume = self._calculate_top_skills_highlights()

        resume.update_work(new_work_resume)
        resume.update_skills(new_skills_resume)
        with open(f"{self.folder}/application_resume.json", "w") as f:
            json.dump(resume.resume_json, f)

    def _get_job_bullets(self):
        with open(f"{self.folder}/bullet_points.json") as f:
            bullets = json.load(f)

        return bullets

    def _calculate_top_work_highlights(self):
        new_work_resume = self.master_resume.resume_json["work"]

        work_highlight_mapping = {
            work.id: work.highlights for work in self.master_resume.work
        }
        work_highlights = ResumeHighlights(work_highlight_mapping, self.job_bullets)

        # Grab different amount of highlights based on how recent the work was
        for i, work in enumerate(self.master_resume.work):
            if i <= 1:
                top_picks = work_highlights.get_top_n_scores_in_section(work.id, n=4)
            elif 2 <= i <= 3:
                top_picks = work_highlights.get_top_n_scores_in_section(work.id, n=2)
            else:
                top_picks = work_highlights.get_top_n_scores_in_section(work.id, n=1)
            print(f"Finished getting {len(top_picks)} top_picks for {work.company}")
            new_work_resume[i]["highlights"] = top_picks

        return new_work_resume

    def _calculate_top_skills_highlights(self):
        new_skills_resume = self.master_resume.resume_json["skills"]

        skills_highlight_mapping = {
            skills.name: skills.keywords for skills in self.master_resume.skills
        }

        skills_highlights = ResumeHighlights(skills_highlight_mapping, self.job_bullets)

        # Grab minimum of 3 for each section
        for i, skills in enumerate(self.master_resume.skills):
            top_picks = skills_highlights.get_top_n_scores_in_section(skills.name, n=3)
            new_skills_resume[i]["keywords"] = top_picks
            print(f"Finished getting {len(top_picks)} top_picks for {skills.name}")

        return new_skills_resume


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--application_name")
    args = parser.parse_args()

    application = Application(args.application_name)
    application.record()
