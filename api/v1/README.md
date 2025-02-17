# AirBnB Clone - API v1

This directory contains version 1 of the AirBnB Clone API.

## Structure
- `views/` - Contains the view modules for various endpoints
- `__init__.py` - Initializes the v1 API with the `app_views` Blueprint
- `app.py` - Main entry point to start the API

## Running the API
To start the API server, run the following command:
```bash
HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd \
HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_dev_db \
HBNB_TYPE_STORAGE=db HBNB_API_HOST=0.0.0.0 HBNB_API_PORT=5000 \
python3 -m api.v1.app

Author: Duncan Korir