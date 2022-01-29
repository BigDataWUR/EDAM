from enum import Enum
import logging

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from edam.reader.models.database import Base, recreate_database

module_logger = logging.getLogger('edam.reader.models')





class StorageType(Enum):
    FILE = 'file'
    MEMORY = 'memory'


if __name__ == "__main__":
    recreate_database()
