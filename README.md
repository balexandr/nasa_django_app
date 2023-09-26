# NASA - Photo of the Day
In this simple Django app, it will reach out to NASA's API and return the title, date and image url for the Astronomy Picture of the Day. 
It will then hit Google's Search API with the APOD title and return some more information (title, snippet). All nicely displayed in the browser.

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
# Start server
python3 manage.py runserver

# Navigate to site to view details
http://127.0.0.1:8000/

# Run tests
python3 manage.py test nasa
```

You'll notice that the raw context dictionary is printed to match task specifications but I figured viewing them in the browser was nicer to look at sans styling.
