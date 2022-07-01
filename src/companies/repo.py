import os
import uuid
from typing import List

import models
import schemas


def get_id():
    return str(uuid.uuid4())


class CompanyRepo:

    def __init__(self):
        self.companies = []
        self.companies.append(models.Company(
            id=get_id(), name="Microsoft", ceo="Satya Nadella", rating=5, industry='Technology'))

    def get(self):
        return self.companies

    def get_by_ceo(self, ceo: str):
        companies = [
            company for company in self.companies if company.ceo == ceo]
        return companies

    def get_by_company_name(self, name: str):
        companies = [
            company for company in self.companies if company.name == name]
        if len(companies) == 0:
            return None
        return companies[0]

    def add_company(self, name, ceo, rating, industry):
        company = self.get_by_company_name(name)
        if company is None:
            company = models.Company(id=get_id(), name=name, ceo=ceo, rating=rating, industry=industry)
            self.companies.append(company)
        return company

CompanyRepoInstance = CompanyRepo()