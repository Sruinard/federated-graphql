import os
import uuid
from typing import List

import models


def get_id():
    return str(uuid.uuid4())


class FounderRepo:

    def __init__(self):
        self.founders = []
        self.founders.append(models.Founder(id=get_id(), name="Satya Nadella"))
        self.founders.append(models.Founder(id=get_id(), name="Jeff Bezos"))

    def get(self):
        return self.founders

    def get_by_name(self, name):
        for founder in self.founders:
            if founder.name == name:
                return founder
        return None

    def add_founder(self, name):
        founder = self.get_by_name(name)
        if founder is None:
            founder = models.Founder(id=get_id(), name=name)
            self.founders.append(founder)
        return founder
