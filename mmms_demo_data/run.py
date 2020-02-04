from datetime import datetime
from multiprocessing import Pool

from company import CompanyTable
from group_contract import GroupContractTable
from member import MemberTable
from member_contract import MemberContractTable
from misc import random_gamma_ceil


num_companies = 100
groups_per_company = 3
num_members = 30000
contracts_per_member = 2


def generate_contracts(index=None):
    companies = CompanyTable(num_companies)
    members = MemberTable(num_members)
    groups = GroupContractTable(companies)
    policies = MemberContractTable(members, groups)
    for c in companies.values():
        for _ in range(random_gamma_ceil(groups_per_company)):
            group = groups.new_group_contract(c)
            policies.new_policy(group_contract=group)

    for m in members.values():
        additional = random_gamma_ceil(contracts_per_member) - len(m["policies"])
        for _ in range(additional):
            policies.new_policy(subscriber=m)

    print(
        f"{index}: {len(companies)} companies, {len(members)} members, {len(groups)} groups, {len(policies)} policies"
    )


start = datetime.now()
pool = Pool()
pool.map(generate_contracts, range(16))
print(f"finished overall in {datetime.now() - start}")
