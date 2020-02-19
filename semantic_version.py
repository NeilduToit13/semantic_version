"""Object that stores a semantic version
And provides for ordering and other operations
"""

from functools import singledispatchmethod, total_ordering

@total_ordering
class SemanticVersion:
    """
    Models Semantic Version objects as described in
    https://semver.org/

    Can be initialised by a string, tuple or keyword arguments:
        SemanticVersion('0.2.4')
        SemanticVersion((2,3,4))
        SemanticVersion(major=4, minor=8, patch=7)

    Ordering operations are implemented to help find latest version.
    """
    def __init__(self, arg=None, major=None, minor=None, patch=None):

        assert bool(arg) ^ all((major is not None, minor is not None, patch is not None))

        if arg is not None:
            self._initialise_from_representation(arg)
        else:
            self.major = major
            self.minor = minor
            self.patch = patch

    @singledispatchmethod
    def _initialise_from_representation(self, arg):
        raise NotImplementedError(
                f"Cannot accept argument of type {type(arg)}"
                )


    @_initialise_from_representation.register
    def _(self, arg: tuple):
        assert len(arg) == 3
        arg = (int(item) for item in arg)

        self.major, self.minor, self.patch = arg


    @_initialise_from_representation.register
    def _(self, arg: str):
        parts = arg.split('.')
        parts = tuple(int(item) for item in parts)

        assert len(parts) == 3

        self.major, self.minor, self.patch = parts


    def to_dict(self):
        return {
            'major': self.major,
            'minor': self.minor,
            'patch': self.patch
            }

    def to_tuple(self):
        return (self.major, self.minor, self.patch)

    def __str__(self):
        """URL safe implementation.
        """
        return f"{self.major}-{self.minor}-{self.patch}"



    def __repr__(self):
        return f"{self.major}.{self.minor}.{self.patch}"



    def __eq__(self, other):
        return self.to_tuple() == other.to_tuple()


    def __le__(self, other):
        return self.to_tuple() <= other.to_tuple()
