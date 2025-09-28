# Prerequisites
- Python 3.12+
- Pip
- Venv

# Set Up Local Environment

1. Create a virtual environment

```bash
python -m venv mijavayr
```

2. Activate the virtual environment

```bash
source mijavayr/bin/activate
```

3. Install the dependencies

```bash
pip install -r requirements.txt
```

4. Run the application

```bash
uvicorn main:app --reload
```