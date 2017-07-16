# This file is part of ranger, the console file manager.
# License: GNU GPL version 3, see the file "AUTHORS" for details.
# pylint: disable=protected-access

from __future__ import (absolute_import, division, print_function)


# Similar to functools.lru_cache of python3
def cached_function(fnc):
    cache = {}

    def inner_cached_function(*args):
        try:
            return cache[args]
        except KeyError:
            value = fnc(*args)
            cache[args] = value
            return value
    inner_cached_function._cache = cache  # pylint: disable=protected-access
    return inner_cached_function


# For use in ranger.vfs:
def cache_until_outdated(function):
    """
    Cache a method until self.modification_time increases

    >>> class File(object):
    ...     def __init__(self):
    ...         self.modification_time = 0
    ...
    ...     @cache_until_outdated
    ...     def get_something(self):
    ...         print('loading...')
    >>> file = File()
    >>> file.get_something()  # should load on the first call
    loading...
    >>> file.get_something()  # shouldn't load, since it's cached already
    >>> file.modification_time = 42  # simulate update
    >>> file.get_something()  # should load again now
    loading...
    >>> file.get_something()  # shouldn't load anymore
    >>> file.modification_time = 23
    >>> file.get_something()  # shouldn't load, since mod time decresased
    >>> file2 = File()
    >>> file2.get_something()
    loading...
    """

    # Set up two dicts, mapping the object instances to the respective value
    function._last_update_time = dict()
    function._cached_value = dict()

    def inner_cached_function(self, *args, **kwargs):
        last_change_time = self.modification_time
        if last_change_time > function._last_update_time.get(self, -1):
            value = function(self, *args, **kwargs)
            function._cached_value[self] = value
            function._last_update_time[self] = last_change_time
            return value

        return function._cached_value[self]

    return inner_cached_function


if __name__ == '__main__':
    import doctest
    doctest.testmod()
