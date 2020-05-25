from app.resume import Resume

from jinja2 import Template

YAML_TEMPLATE = """/* #*/ export const PERSON = `
name: {{ r.basics.name }}
about: {{ r.basics.summary }}
position: {{ r.basics.label }}
contact:
  email: {{ r.basics.email }}
  city: {{ r.basics.location }}
  website: {{ r.basics.website }}
  {% for profile in r.basics.profiles -%}
  {{ profile.network | lower }}: {{ profile.username }}
  {% endfor %}
lang: en

experience:
{%- for job in r.work %}
- company: {{ job.company }}
  position: {{ job.position }}
  timeperiod: {{ job.startDate }} - {{ job.endDate }}
  description:
    {%- for highlight in job.highlights %}
    - {{ highlight }}
    {%- endfor %}
{% endfor %}

education:
{%- for school in r.education %}
- degree: {{ school.studyType }} {{ school.area }}
  institution: {{ school.institution }}
  timeperiod: {{ school.startDate }} - {{ school.endDate }}
  {% if school.thesis -%}
  thesis: {{ school.thesis }}
  {%- endif %}
  {% if school.publications -%}
  publications: {{ school.publications }}
  {%- endif %}
{% endfor %}

skills:
{%- for skill in r.skills %}
- name: {{ skill.name }}
  highlights:
    {%- for highlight in skill.keywords %}
    - {{ highlight }}
    {%- endfor %}
{% endfor -%}
`"""


def convert_to_yaml(resume_file, output_yaml):
    resume = Resume(resume_file)
    print(f"Loaded {resume.resume_file}")

    template = Template(YAML_TEMPLATE)
    with open(output_yaml, "w") as f:
        f.write(template.render(r=resume))
    print(f"Wrote Yaml file:")
    print(f"    {output_yaml}")
