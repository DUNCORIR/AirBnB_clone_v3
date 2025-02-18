#!/usr/bin/python3
"""
Module for initializing the models package.

This module sets up the storage engine based on the environment configuration.
It supports both FileStorage (for file-based storage)
and DBStorage (for database storage).
"""

from os import getenv


storage_t = getenv("HBNB_TYPE_STORAGE")

if storage_t == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
