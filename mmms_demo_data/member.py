from faker import Faker

from random_access_table import RandomAccessTable


class MemberTable(RandomAccessTable):
    def __init__(self, size=0):
        super().__init__()
        self.fake = Faker()

        for _ in range(size):
            self.new_member()

    def new_member_id(self):
        member_id = self.fake.isbn10()
        while member_id in self:
            member_id = self.fake.isbn10()
        return member_id

    def new_member(self, member_id=None):
        if member_id is None:
            member_id = self.new_member_id()

        member = self.fake.profile(
            ["name", "ssn", "birthdate", "sex", "mail", "address"]
        )
        member["member_id"] = member_id
        member["policies"] = []
        self[member_id] = member
        return member
