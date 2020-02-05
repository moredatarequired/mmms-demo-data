from datetime import datetime
from multiprocessing import Pool

import click
from faker import Faker

from company import CompanyTable
from connect import connect_to_mongodb
from group_contract import GroupContractTable
from member import MemberTable
from member_contract import MemberContractTable
from misc import random_gamma_ceil, random_seed


class ContractSet:
    def __init__(
        self, fake, num_companies, num_members, groups_per_company=10, contracts_per_member=2
    ):
        self.companies = CompanyTable(fake, num_companies)
        self.members = MemberTable(fake, num_members)
        self.groups = GroupContractTable(fake, self.companies)
        self.policies = MemberContractTable(fake, self.members, self.groups)

        for c in self.companies.values():
            for _ in range(random_gamma_ceil(groups_per_company)):
                group = self.groups.new_group_contract(c)
                self.policies.new_policy(group_contract=group)

        for m in self.members.values():
            additional = random_gamma_ceil(contracts_per_member) - len(m["policies"])
            for _ in range(additional):
                self.policies.new_policy(subscriber=m)

    def write_to_mongo(self):
        client = connect_to_mongodb()
        db = client.insurance_demo
        db.companies.insert_many(self.companies.values())
        db.members.insert_many(self.members.values())
        db.groups.insert_many(self.groups.values())
        db.policies.insert_many(self.policies.values())


def create_batch(num_members):
    fake = Faker()
    fake.seed_instance(random_seed())
    start = datetime.now()
    cs = ContractSet(fake, num_members // 300, num_members)
    generated = datetime.now()
    print(f"created contracts in {generated - start}")
    cs.write_to_mongo()
    print(f"wrote collection to mongo in {datetime.now() - generated}")


@click.command()
@click.option('--total_members', default=40000, help='Number of members to add.')
@click.option('--batch_size', default=10000, help='Number of members to generate per batch.')
def create_in_parallel(total_members, batch_size):
    start = datetime.now()
    pool = Pool()
    pool.map(create_batch, [batch_size for _ in range(total_members // batch_size)])
    print(f"finished overall in {datetime.now() - start}")

if __name__ == '__main__':
    create_in_parallel()
