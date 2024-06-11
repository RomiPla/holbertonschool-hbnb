
from abc import ABC
import datetime
from uuid import uuid4

class Basemodel(ABC):
    def __init__(self):
        self.id = uuid4()
        self.create_at = datetime.datetime.now()
        self.update_at = datetime.datetime.now()

    def save(self):
        self.update_at = datetime.datetime.now()

