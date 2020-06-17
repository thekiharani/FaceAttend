# FaceAttend

## Quick Start

- Install the required in a virtual environment (preferred) or system python: `pip install -r requirements.txt`
- Activate the virtual environment (if applicable)
    - I used `anaconda` python package because `pip` and `pipenv` was giving me some issues. But with the current `requirements.txt` file, either should work
- Migrate the database models: `python manage.py migrate`
- Run the dev server: `python manage.py runserver`
- `That should be it`