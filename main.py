from app.resume import Resume
from config import OUTPUT_YAML, RESUME_FILE
from resume_generator.pdf.json_to_yaml import convert_to_yaml


def main():
    convert_to_yaml(resume_file=RESUME_FILE, output_yaml=OUTPUT_YAML)


if __name__ == "__main__":
    main()
