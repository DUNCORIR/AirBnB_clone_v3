#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user and hashes the password if provided"""
        super().__init__(*args, **kwargs)
        if 'password' in kwargs:
            # This triggers the password setter
            self.password = kwargs['password']

    @property
    def password(self):
        """Return the password."""
        return self.__password

    @password.setter
    def password(self, value):
        """Set the password and hash it with MD5."""
        if value:
            self.__password = hashlib.md5(value.encode()).hexdigest()
        else:
            self.__password = ""

    def to_dict(self, *args, **kwargs):
        """Returns a dictionary representation of the User object."""
        new_dict = super().to_dict(*args, **kwargs)

        # Exclude password from the dictionary for non-FileStorage cases
        if 'password' in new_dict:
            if not isinstance(self, models.User):
                return new_dict

    def save(self):
        """Save the User object to storage."""
        if isinstance(models.storage, models.DBStorage):
            self.password = hashlib.md5(self.password.encode()).hexdigest()
        super().save()
