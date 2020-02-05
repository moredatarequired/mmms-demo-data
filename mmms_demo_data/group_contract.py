from misc import random_date_range
from random_access_table import RandomAccessTable


class GroupContractTable(RandomAccessTable):
    def __init__(self, fake, company_table, size=0):
        self.fake = fake
        super().__init__()
        self.companies = company_table

        for _ in range(size):
            self.new_group_contract()

    def new_group_contract(self, company=None):
        group_contract_id = self.random_unused_key()

        if company is None:
            company = self.companies.random()

        start_date, end_date = random_date_range(self.fake)
        contract = {
            "_id": group_contract_id,
            "company_id": company["_id"],
            "start_date": start_date,
            "end_date": end_date,
            "policies": [],
        }
        # Update the company to include this group contract.
        company["group_contracts"].append(group_contract_id)
        self[group_contract_id] = contract
        return contract
