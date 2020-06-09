# Resume Generator

Repo with master resume.json and related scripts. I use [Best Resume Ever](https://github.com/salomonelli/best-resume-ever) with a [custom template](https://github.com/ericmjalbert/best-resume-ever/blob/master/src/resumes/eric-jalbert.vue) to generate the PDF resume.

The real goody to this project is that it uses a [pre-trained Tensorhub model](https://tfhub.dev/google/universal-sentence-encoder/4) to modify my resume based on the bullet points of a job description.

Here is an example of the whole script in action:

![make application example](/assets/example_application.gif)

# Usage

## Installation

There are 3 things that need to be done for installation:
1. `git clone` and install my fork of [Best Resume Ever](https://github.com/ericmjalbert/best-resume-ever); alternatively you can use your own fork of the repo. Once this is installed, update the value of `BEST_RESUME_EVER_PATH` in [`config.py`](./config.py). Something like this should help guide how to do it (don't run this blindly!):
```bash
cd ../
git clone https://github.com/ericmjalbert/best-resume-ever
cd best_resume_ever
npm install
cd ../resume-generator
sed -ie "s#/Users/ericjalbert/Documents/eric_stuff/best-resume-ever#$(pwd)/../best-resume-ever#g" config.py
```

2. You need to get the venv all setup. Ensure you have a system python version that is `>=3.7` (since we use dataclass).
```bash
make init
```

3. You need to get the tensorhub sentence encoder downloaded. This might take 5-10 mins depending on internet (about 1 GB download).
```bash
make init_encoder
```

Once it's finished running you're ready to work! Check the makefile help for usage instructions:
```bash
make help
```

*NOTE*: Resume data is stored in `master_resume/resume.json`. Be sure to change this to your own resume before real usage.


## Running tests

We use pytest to manage all the tests for this project. They can be run by:
```bash
make tests
```

or, for the slower end-to-end test (~2 mins):
```bash
make tests_full
```

## Adding new packages

We use [pip-tools](https://github.com/jazzband/pip-tools) to manage packages. This means that to add a new package it needs to be added to `requirements.in` and then we need to compile a new `requirements.txt`. All of this is wrapped up in the `make init` function so that has be to run after each addition to `requirements.in`

# Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

# License
[MIT](https://choosealicense.com/licenses/mit/)
