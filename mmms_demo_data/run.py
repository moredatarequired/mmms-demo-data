from datetime import datetime
from multiprocessing import Pool

from member import MemberTable


def create_subtable(n):
    start = datetime.now()
    members = MemberTable(n)
    print(f"created {len(members)} in {datetime.now() - start}")


start = datetime.now()
pool = Pool()
pool.map(create_subtable, [10000] * 16)
print(f"finished overall in {datetime.now() - start}")
