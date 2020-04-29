# ericmjalbert-resume

Repo with master resume.json and related scripts

## Installation

Create a Python `venv` that is version `>=3.7` (since we use dataclass)
```bash
virtualenv venv3 --python python3.7
```

Install all packaged:
```bash
venv/bin/pip install -r requirements.txt
```

Now you're ready to work!

## Usage

Make sure that the data in `resume/resume.json` is updated to reflect your own work.

```python
```

### Adding new packages

We use (pip-tools)[https://github.com/jazzband/pip-tools] to manage packaged. This means that to add a new package it needs to be added to `requirements.in` and then we need to compile a new `requirements.txt`:
```bash
venv/bin/python -m piptools compile
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
