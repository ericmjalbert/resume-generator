# ericmjalbert-resume

Repo with master resume.json and related scripts. I use [Best Resume Ever](https://github.com/salomonelli/best-resume-ever) with a [custom template](./resume_generator/pdf/templates/eric-jalbert.vue) to generate the PDF resume.

## Installation

Ensure you have a system python version that is `>=3.7` (since we use dataclass)
```bash
make init
```

The above make command will create the venv and initialize it with the needed packages.
Once it's finished running you're ready to work!

### PDF export
For the PDF exports to work you need to have [Best Resume Ever](https://github.com/salomonelli/best-resume-ever) installed and working. Before running `make pdf` just make sure you have `BEST_RESUME_EVER_ABS_PATH=/path/to/best-resume-ever`, for example:
```bash
BEST_RESUME_EVER_ABS_PATH="/Users/ericjalbert/Documents/eric_stuff/best-resume-ever" make pdf
```


## Usage

Make sure that the data in `resume/resume.json` is updated to reflect your own work.

```python
venv/bin/python main.py
```

### Running tests

We use pytest to manage all the tests for this project. They can be run by:
```bash
make tests
```

### Adding new packages

We use (pip-tools)[https://github.com/jazzband/pip-tools] to manage packaged. This means that to add a new package it needs to be added to `requirements.in` and then we need to compile a new `requirements.txt`:
```bash
venv/bin/python -m piptools compile
```

then make sure you redo the pip install:
```bash
venv/bin/pip install -r requirements.txt
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)



### TODO
[ ] Make a public fork of the best-resume-ever repo with my eric-jalbert template in it.
