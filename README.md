# Coding Assignment for Kisanhub

## Problem statement
Create a Django app using DRF to store and retrieve UK weather data.
The source data comes from the [UK Metoffice](https://www.metoffice.gov.uk/climate/uk/summaries/datasets#yearOrdered)

For convenience we’ve scraped this into JSON files on AWS S3.

There are three metrics: Tmax (max temperature), Tmin (min temperature) and Rainfall (mm), and 4 locations: UK, England, Scotland, Wales.

The url format on S3 is:

https://s3.eu-west-2.amazonaws.com/interview-question-data/metoffice/{metric}-{location}.json

E.g:

https://s3.eu-west-2.amazonaws.com/interview-question-data/metoffice/Rainfall-England.json

(Note that Jan=1, Dec=12)


### Prerequisites
- Django 2.1
- Python 3.5
- PostgreSQL 9.5

### REST API
1. GET endpoint '<domain>/api/v1/metric/'
```
    - @param start_date: date in format YYYY-MM-DD
    - @param end_date: date in format YYYY-MM-DD
    - @param type: "Tmax", "Tmin" and "Rainfall" as type
    - @param location: "UK", "England", "Wales" and "Scotland" as location
```

2. POST endpoint '<domain>/api/v1/metric/'
```
    - @param data: list of dict as shown [here](https://s3.eu-west-2.amazonaws.com/interview-question-data/metoffice/Rainfall-England.json)
    - @param type: "Tmax", "Tmin" and "Rainfall" as type
    - @param location: "UK", "England", "Wales" and "Scotland" as location
```

### Management command
1. Run following command to fetch data from S3 urls and write to Django server via API and read this data back and confirm that it's same data.
    - ```python manage.py createdatabase```