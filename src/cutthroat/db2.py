import logging
from collections import MutableMapping


def stringify_list(l):
    """Stringify list `l`

    :returns: A comma-joined string rep of `l`
    :rtype: str
    """
    return ",".join(map(str, l))


def listify_string(func, s):
    """'Decode' `s` into a list

    :returns: A list of elements from a comma-split of s each wrapped
        with func
    :rtype: list
    """
    if not s:
        return []
    else:
        return map(func, s.split(","))


class NotFoundError(Exception):

    """NotFoundError"""


class IllegalDeleteError(Exception):

    """IllegalDeleteError"""


class DBObjectMapping(MutableMapping):

    """Base class for objects mapping to the database

    All classes subclassing from this should:
    - Define an initialize method; it doesn't have to do anything
    - Define an r_transform method
    - Define an w_transform method
    - Be named the CapWords singular noun version of the DB table they access
    """

    def __init__(self, db, attr_key, attr_val):
        self.attr_key = attr_key
        self.attr_val = attr_val
        self.__find_d = {attr_key: self.w_transform(attr_key, attr_val)}
        self.__db = db
        self.initialize()
        # Call __store to assert that object with attr_key of attr_val exists
        self.__store

    @property
    def _table_name(self):
        return "{}s".format(self.__class__.__name__.lower())

    @property
    def __store(self):
        p = self.__db[self._table_name].find_one(
            **self.__find_d)
        if not p:
            raise NotFoundError
        logging.debug(p.items())
        return {k: self.r_transform(k, v) for k, v in p.items()}

    def __getitem__(self, key):
        return self.__store[key]

    def initialize(self):
        raise NotImplementedError

    def r_transform(self, key, value):
        """Transforms value based on key for reading from the DB"""
        raise NotImplementedError

    def w_transform(self, key, value):
        """Transforms value based on key for writing to the DB"""
        raise NotImplementedError

    def __setitem__(self, key, value):
        if key == self.attr_key:
            raise AttributeError(
                "Cannot modify current identifier while it is still the"
                " identifier of the object."
            )
        self.__db[self._table_name].update(
            {
                self.attr_key: self.w_transform(self.attr_key, self.attr_val),
                key: self.w_transform(key, value)
            },
            [self.attr_key]
        )

    def __iter__(self):
        return iter(self.__store)

    def __len__(self):
        return len(self.__store)

    def __delitem__(self, key):
        raise IllegalDeleteError("Deleting attributes from DB is disallowed.")

    def __repr__(self):
        return repr(self.__store)

    def __str__(self):
        return self.__repr__()


class Player(DBObjectMapping):

    def initialize(self):
        pass

    def r_transform(self, key, value):
        if key in ["balls", "orig_balls"]:
            value = listify_string(int, value)
        return value

    def w_transform(self, key, value):
        if key in ["balls", "orig_balls"]:
            value = stringify_list(value)
        return value


class Room(DBObjectMapping):

    def initialize(self):
        pass

    def r_transform(self, key, value):
        if key in ["current_players"]:
            value = listify_string(str, value)
        return value

    def w_transform(self, key, value):
        if key in ["current_players"]:
            value = stringify_list(value)
        return value


class Game(DBObjectMapping):

    def initialize(self):
        pass

    def r_transform(self, key, value):
        if key in ["unclaimed_balls", "orig_unclaimed_balls"]:
            value = listify_string(int, value)
        elif key in ["players"]:
            value = listify_string(str, value)
        return value

    def w_transform(self, key, value):
        if key in ["unclaimed_balls", "players", "orig_unclaimed_balls"]:
            value = stringify_list(value)
        return value
