from faker import Faker

from random_access_table import RandomAccessTable


class MemberTable(RandomAccessTable):
    def __init__(self, size=0):
        self.fake = Faker()
        super().__init__(key_gen=self.fake.isbn10)

        for _ in range(size):
            self.new_member()

    def new_member(self, member_id=None):
        if member_id is None:
            member_id = self.random_unused_key()

        member = self.fake.profile(
            ["name", "ssn", "birthdate", "sex", "mail", "address"]
        )
        member["member_id"] = member_id
        member["policies"] = []
        self[member_id] = member
        return member
