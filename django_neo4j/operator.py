# coding=utf-8
import decimal

import six


class Operator(object):
    """
    http://neo4j.com/docs/stable/query-operators.html
    """

    UNARY = 1
    BINARY = 2

    _ARITY_NAMES = (u'unary', u'binary')

    def __init__(self, name, symbol, arity=None):
        super(Operator, self).__init__()

        # NAME
        if not name:
            raise ValueError(u'name must be set')

        # SYMBOL
        if not symbol:
            raise ValueError(u'symbol must be set')

        # ARITY
        arity = arity or self.BINARY
        if arity not in (self.UNARY, self.BINARY):
            raise ValueError(u'arity may only be 1 or 2')

        # SET
        self.__type = self.__class__.__name__.lstrip(u'_')
        self.__name = name
        self.__symbol = symbol
        self.__arity = arity or self.BINARY
        self.__arity_name = self._ARITY_NAMES[arity - 1]

    @property
    def type(self):
        return self.__type

    @property
    def name(self):
        return self.__name

    @property
    def symbol(self):
        return self.__symbol

    @property
    def arity(self):
        return self.__arity

    @property
    def arity_name(self):
        return self.__arity_name

    @property
    def is_unary(self):
        return self.__arity == self.UNARY

    @property
    def is_binary(self):
        return self.__arity == self.BINARY

    def _validate(self, o):
        raise NotImplemented

    def _check_lhs(self, lhs):
        pass

    def _check_rhs(self, rhs):
        pass

    def _unary(self, a):
        raise NotImplemented

    def __unary(self, a):
        self._check_lhs(a)
        return self._unary(
            str(self._validate(a))
        )

    def _binary(self, a, b):
        raise NotImplemented

    def __binary(self, a, b):
        self._check_lhs(a)
        self._check_rhs(b)
        return self._binary(
            str(self._validate(a)),
            str(self._validate(b)),
        )

    def __call__(self, *args):
        if len(args) != self.arity:
            raise ValueError(u'invalid arity: operator {} is {}: {} argument(s) specified'.format(
                self.name,
                self.arity_name,
                len(args),
            ))

        if self.is_unary:
            return self.__unary(*args)

        if self.is_binary:
            return self.__binary(*args)


# MATHEMATICAL
####################

class _Mathematical(Operator):
    __valid_types = tuple(list(six.integer_types) + [float, decimal.Decimal])

    def __init__(self, name, symbol, arity=None, check_lhs=None, check_rhs=None):
        super(_Mathematical, self).__init__(name, symbol, arity)
        self._check_lhs = check_lhs or self._check_lhs
        self._check_rhs = check_rhs or self._check_rhs

    def _validate(self, a):
        if not isinstance(a, self.__valid_types):
            raise ValueError(u'argument not of type: {}'.format(self.__valid_types))
        return a

    def _binary(self, a, b):
        return u'{}{}{}'.format(a, self.symbol, b)


def _divide_by_zero_check(rhs):
    if rhs == 0:
        raise ZeroDivisionError


class Mathematical(object):
    __add = _Mathematical(name=u'add', symbol=u'+')
    __subtract = _Mathematical(name=u'subtract', symbol=u'-')
    __multiply = _Mathematical(name=u'multiply', symbol=u'*')
    __divide = _Mathematical(name=u'divide', symbol=u'/', check_rhs=_divide_by_zero_check)
    __mod = _Mathematical(name=u'mod', symbol=u'%')
    __pow = _Mathematical(name=u'pow', symbol=u'^')

    @property
    def add(self):
        return self.__add

    @property
    def subtract(self):
        return self.__subtract

    @property
    def multiply(self):
        return self.__multiply

    @property
    def divide(self):
        return self.__divide

    @property
    def mod(self):
        return self.__mod

    @property
    def pow(self):
        return self.__pow


# COMPARISON
####################

class _Comparison(Operator):
    pass


class Comparison(object):
    pass


# BOOLEAN
####################

class _Boolean(Operator):
    pass


class Boolean(object):
    pass


# STRING
####################


class _String(Operator):
    pass


class String(object):
    pass


# COLLECTION
####################
class _Collection(Operator):
    pass


class Collection(object):
    pass


# REGEX
####################


class _Regex(Operator):
    pass


class Regex(object):
    pass


# noinspection PyPep8Naming
class ops(object):
    mathematical = Mathematical()
    math = mathematical
    m = mathematical

    comparison = Comparison()
    compare = comparison
    c = comparison

    boolean = Boolean()
    b = boolean

    string = String()
    s = string

    collection = Collection()
    collect = collection
    C = collection

    regex = Regex()
    r = regex
