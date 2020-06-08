import argparse

from config import OUTPUT_YAML, JOB_APP_FOLDER_TEMPLATE

from resume_generator.general.application import Application
from resume_generator.general.job_description import JobDescription
from resume_generator.pdf.json_to_yaml import convert_to_yaml


JOB_PARSE = "get_job_bullets"
BUILD_RESUME_JSON = "build_resume_json"
BUILD_RESUME_YAML = "build_resume_yaml"
COMMANDS = [JOB_PARSE, BUILD_RESUME_JSON, BUILD_RESUME_YAML]

parser = argparse.ArgumentParser()
parser.add_argument("command", choices=COMMANDS)
parser.add_argument("--application_name", required=False)
parser.add_argument("--url", required=False)
parser.add_argument("--rebuild", required=False, action="store_true")
args = parser.parse_args()


folder = JOB_APP_FOLDER_TEMPLATE.format(application_name=args.application_name)

if args.command == JOB_PARSE:
    if not args.rebuild:
        job = JobDescription(application_name=args.application_name, url=args.url)
    else:
        job = JobDescription(
            application_name=args.application_name,
            html_file=f"{folder}/site_content.html",
        )
    job.record()

if args.command == BUILD_RESUME_JSON:
    print(f"Creating Application instance for {args.application_name}")
    app = Application(application_name=args.application_name, rebuild=args.rebuild)
    print(f"Recording custom application resume_json")
    app.record()

if args.command == BUILD_RESUME_YAML:
    convert_to_yaml(f"{folder}/application_resume.json", OUTPUT_YAML)
