import random

from bson.objectid import ObjectId


class RandomAccessTable:
    def __init__(self, key_gen=None):
        self.items = []
        self.lookup = {}
        self.key_gen = key_gen if key_gen else ObjectId

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

    def random_unused_key(self):
        new_key = self.key_gen()
        while new_key in self:
            new_key = self.key_gen()
        return new_key

    def values(self):
        return self.items

    def random(self, n=1, with_replacement=False):
        if n == 1:
            return random.choice(self.items)
        if with_replacement:
            return random.choices(self.items, k=n)
        else:
            return random.sample(self.items, k=n)
