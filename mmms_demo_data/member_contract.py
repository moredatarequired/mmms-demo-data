import random

from misc import random_date_range
from random_access_table import RandomAccessTable


class MemberContractTable(RandomAccessTable):
    def __init__(self, fake, members, group_contracts, avg_beneficiaries=1, size=0):
        self.fake = fake
        super().__init__()
        self.members = members
        self.group_contracts = group_contracts
        self.avg_beneficiaries = avg_beneficiaries

        for _ in range(size):
            self.new_policy()

    def num_beneficiaries(self):
        return int(random.expovariate(self.avg_beneficiaries + 0.5))

    def new_policy(self, group_contract=None, subscriber=None, beneficiaries=None):
        member_contract_id = self.random_unused_key()

        if group_contract is None:
            group_contract = self.group_contracts.random()
        group_contract["policies"].append(member_contract_id)

        start, end = group_contract["start_date"], group_contract["end_date"]
        start_date, end_date = random_date_range(self.fake, start, end)

        if subscriber is None:
            subscriber = self.members.random()
        subscriber["policies"].append(member_contract_id)

        if beneficiaries is None:
            beneficiaries = self.members.random(n=self.num_beneficiaries())
        for b in beneficiaries:
            b["beneficiary_of"].append(member_contract_id)

        policy = {
            "_id": member_contract_id,
            "group_contract_id": group_contract["_id"],
            "subscriber": subscriber["_id"],
            "beneficiaries": [b["_id"] for b in beneficiaries],
            "start_date": start_date,
            "end_date": end_date,
        }
        self[member_contract_id] = policy
        return policy
