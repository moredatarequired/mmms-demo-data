from misc import to_datetime
from random_access_table import RandomAccessTable


class MemberTable(RandomAccessTable):
    def __init__(self, fake, size=0):
        self.fake = fake
        super().__init__()

        for _ in range(size):
            self.new_member()

    def new_member(self):
        member_id = self.random_unused_key()

        member = self.fake.profile(
            ["name", "ssn", "birthdate", "sex", "mail", "address"]
        )
        member["birthdate"] = to_datetime(member["birthdate"])
        member["_id"] = member_id
        member["policies"] = []
        member["beneficiary_of"] = []
        self[member_id] = member
        return member
