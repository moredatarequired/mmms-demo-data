from faker import Faker

from random_access_table import RandomAccessTable


class CompanyTable(RandomAccessTable):
    def __init__(self, size=0):
        self.fake = Faker()
        super().__init__(key_gen=self.fake.ein)

        for _ in range(size):
            self.new_company()

    def new_company(self, company_id=None):
        if company_id is None:
            company_id = self.random_unused_key()

        company = {
            "company_name": self.fake.company(),
            "address": self.fake.address(),
            "contact_email": self.fake.company_email(),
            "contact_phone": self.fake.phone_number(),
            "company_id": company_id,
            "group_contracts": [],
        }
        self[company_id] = company
        return company
