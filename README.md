This application exists to aid in creating a dataset of [vk.com](https://vk.com) user profiles.

The service is inteded to run periodically, for example as a cron job.

# Intended workflow

1. [vk.com](https://vk.com) profile links are submitted to a Google forms form and stored in a spreadsheet
2. Links are downloaded using Google Drive API
3. Each link is parsed, profile information is retrieved
4. Profile information is stored in a local database

# Running the service

The service expects a `local_settings.py` to be included.
The following global variables have to be set in it:
```python
VK_SERVICE_KEY = '' # vk.com API service key
GOOGLE_API_KEY_FILE = '' # Google API json credentials file location
GOOGLE_SPREADSHEET = "" # Name of the spreadsheet to parse
RECORDS_AFTER_FILE_LOCATION = 'records_after' # path to a file to store the amount of already parsed records in the spreadsheet, can be anywhere
DB_LOCATION = '' # Path to database file
LOG_LOCATION = '' # Path to log file

LOGGER = logging.getLogger('my_logger') # Logger configuration. Put all handlers and formatters here too.
```
A template `sample_local_settings.py` file is provided, you can copy it and rename it to `local_settings.py` for convinience.

Next, install the dependencies:
```
pip install -r requirements.txt
```

Run tests via pytest:
```
pytest -q tests
```

And run!
```
python profile_extractor.py
```
