import random
from datetime import date, datetime, timedelta
from pprint import pprint

from bson.objectid import ObjectId
from faker import Faker

fake = Faker()


class Table:
    def __init__(self):
        self.items = []
        self.lookup = {}

    def __contains__(self, key):
        return key in self.lookup

    def __getitem__(self, key):
        index = self.lookup[key]
        return self.items[index]

    def __setitem__(self, key, value):
        index = self.lookup.get(key)
        if index:
            self.items[index] = value
        else:
            self.lookup[key] = len(self.items)
            self.items.append(value)

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return iter(self.lookup)

    def values(self):
        return self.items

    def random(self, n=1, with_replacement=False):
        if n == 1:
            return random.choice(self.items)
        if with_replacement:
            return random.choices(self.items, k=n)
        else:
            return random.sample(self.items, k=n)


def random_date_range(start=None, end=None):
    if start is None:
        start = date(year=1972, month=1, day=1)  # Arbitrary start date.
    if end is None:
        end = date.today() + timedelta(days=3650)

    start_date = fake.date_between(start_date=start, end_date=end)
    end_date = fake.date_between(start_date=start_date, end_date=end)

    if end_date > date.today() + timedelta(days=365):
        end_date = None

    return start_date, end_date


# Step 1: create N companies.
num_companies = 100
companies = Table()


def new_company():
    company_id = fake.ein()
    while company_id in companies:
        company_id = fake.ein()

    company = {
        "company_name": fake.company(),
        "address": fake.address(),
        "contact_email": fake.company_email(),
        "contact_phone": fake.phone_number(),
        "company_id": company_id,
        "group_contracts": [],
    }
    companies[company_id] = company
    return company


start_company_generation = datetime.now()
for _ in range(num_companies):
    new_company()

duration = datetime.now() - start_company_generation
print(f"generated {len(companies)} companies in {duration}")


# Step 2: create at least one group contract for each company

group_contracts = Table()


def new_group_contract(company=None):
    group_contract_id = fake.msisdn()
    while group_contract_id in group_contracts:
        group_contract_id = fake.msisdn()

    if company is None:
        company = companies.random()

    start_date, end_date = random_date_range()
    contract = {
        "group_contract_id": group_contract_id,
        "company_id": company["company_id"],
        "start_date": start_date,
        "end_date": end_date,
        "policies": [],
    }
    group_contracts[group_contract_id] = contract
    # Add this contract back to the group.
    company["group_contracts"].append(group_contract_id)
    return contract


start_group_generation = datetime.now()
for company in companies.values():
    new_group_contract(company)

average_groups_per_company = 3
num_extra_groups = num_companies * (average_groups_per_company - 1)

for company in companies.random(n=num_extra_groups, with_replacement=True):
    new_group_contract()  # And the extra random ones, for good measure.

duration = datetime.now() - start_group_generation
print(f"generated {len(group_contracts)} group contracts in {duration}")


members = Table()


def new_member():
    member_id = fake.isbn10()
    while member_id in members:
        member_id = fake.isbn10()

    member = fake.profile(["name", "ssn", "birthdate", "sex", "mail", "address"])
    member["member_id"] = member_id
    member["policies"] = []
    members[member_id] = member
    return member


policies = Table()

average_beneficiaries = 1


def new_policy(group_contract=None, subscriber=None, beneficiaries=None, create=True):
    policy_id = fake.isbn13()
    while policy_id in policies:
        policy_id = fake.isbn13()

    if group_contract is None:
        group_contract = group_contracts.random()

    start, end = group_contract["start_date"], group_contract["end_date"]
    start_date, end_date = random_date_range(start, end)

    if subscriber is None:
        subscriber = new_member() if create else members.random()
    subscriber["policies"].append(policy_id)

    if beneficiaries is None:
        num = int(random.expovariate(average_beneficiaries + 0.5))
        beneficiaries = [
            new_member() if create else members.random() for _ in range(num)
        ]
    for b in beneficiaries:
        b["policies"].append(policy_id)

    policy = {
        "policy_id": policy_id,
        "group_contract_id": group_contract["group_contract_id"],
        "subscriber": subscriber["member_id"],
        "beneficiaries": [b["member_id"] for b in beneficiaries],
        "start_date": start_date,
        "end_date": end_date,
    }
    policies[policy_id] = policy
    return policy


# Step 3: create member contracts (and members) for each group contract.

average_policies_per_group = 300

start_policy_member_generation = datetime.now()
for ct in group_contracts.values():
    for _ in range(int(random.gammavariate(average_policies_per_group, 1))):
        new_policy(group_contract=ct)

duration = datetime.now() - start_policy_member_generation
print(f"generated {len(policies)} policies and {len(members)} members in {duration}")

# Step 4: add more member contracts, reusing members:

start_policy_generation = datetime.now()
for _ in range(len(members)):
    new_policy(create=False)

duration = datetime.now() - start_policy_generation
print(f"generated to {len(policies)} policies in {duration}")
