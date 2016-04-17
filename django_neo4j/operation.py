# coding=utf-8
import decimal

import six

from django_neo4j.exception import OperationArgumentTypeError, OperationArgumentMismatchError, OperationArityError, \
    OperationZeroDivisionError, OperationInitializationError, OperationImplementationError
from django_neo4j.type import NULL


def _wrap_string(o):
    return u'"{}"'.format(o) if isinstance(o, (str, unicode)) else o

def _reverse_binary(self, a, b):
    self._binary(b, a)


class Operation(object):
    """
    http://neo4j.com/docs/stable/query-operations.html
    """

    UNARY = 1
    BINARY = 2

    _ARITY_NAMES = (u'unary', u'binary')

    def __init__(
        self,
        name,
        symbol,
        valid_types=None,
        arity=None
    ):
        super(Operation, self).__init__()

        # NAME
        if not name:
            raise OperationInitializationError(self, u'name must be set')

        # SYMBOL
        if not symbol:
            raise OperationInitializationError(self, u'symbol must be set')

        # ARITY
        arity = arity or self.BINARY
        if arity not in (self.UNARY, self.BINARY):
            raise OperationInitializationError(self, u'arity may only be 1 or 2')

        # SET
        self.__type = self.__class__.__name__.lstrip(u'_')
        self.__name = name
        self.__symbol = symbol
        self.__arity = arity or self.BINARY
        self.__arity_name = self._ARITY_NAMES[arity - 1]
        self.__valid_types = tuple(valid_types or [])

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

    @property
    def valid_types(self):
        return self.__valid_types

    def _type_check(self, *args):
        for arg in args:
            if self.valid_types and not isinstance(arg, self.valid_types):
                raise OperationArgumentTypeError(self, arg)

    def _validate(self, *args):
        return args

    def _unary(self, a):
        raise OperationImplementationError(self, '_unary')

    def __unary(self, a):
        return self._unary(*self.__validate(a))

    def _binary(self, a, b):
        raise OperationImplementationError(self, '_binary')

    def __validate(self, *args):
        self._type_check(*args)
        clean_args = [six.u(arg) if isinstance(arg, str) else arg for arg in args]
        return self._validate(*clean_args)

    def __binary(self, a, b):
        return self._binary(*self.__validate(a, b))

    def __call__(self, *args):
        if len(args) != self.arity:
            raise OperationArityError(self, len(args))

        if self.is_unary:
            return self.__unary(*args)

        if self.is_binary:
            return self.__binary(*args)


# MATHEMATICAL
####################

class _Mathematical(Operation):
    def __init__(self, name, symbol, arity=None):
        super(_Mathematical, self).__init__(
            name=name,
            symbol=symbol,
            valid_types=list(six.integer_types) + [float, decimal.Decimal],
            arity=arity,
        )

    def _binary(self, a, b):
        return u'{}{}{}'.format(_wrap_string(a), self.symbol, _wrap_string(b))


class _DivideMathematicalOperation(_Mathematical):
    def __init__(self):
        super(_DivideMathematicalOperation, self).__init__(name=u'divide', symbol=u'/')

    def _validate(self, *args):
        args = super(_DivideMathematicalOperation, self)._validate(*args)
        if args[1] == 0:
            raise OperationZeroDivisionError
        return args


class Mathematical(object):
    __add = _Mathematical(name=u'add', symbol=u'+')
    __subtract = _Mathematical(name=u'subtract', symbol=u'-')
    __multiply = _Mathematical(name=u'multiply', symbol=u'*')
    __divide = _DivideMathematicalOperation()
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

class _Comparison(Operation):
    def __init__(self, name, symbol, arity=None):
        super(_Comparison, self).__init__(
            name=name,
            symbol=symbol,
            valid_types=list(six.integer_types) + [float, decimal.Decimal, str, unicode, type(NULL)],
            arity=arity,
        )

    def _validate(self, *args):
        args = super(_Comparison, self)._validate(*args)
        if self.is_binary:
            a, b = args
            if isinstance(a, (str, unicode)) != isinstance(b, (str, unicode)):
                raise OperationArgumentMismatchError(self, a, b)

        return args

    def _unary(self, a):
        return u'{}{}'.format(_wrap_string(a), self.symbol)

    def _binary(self, a, b):
        return u'{}{}{}'.format(_wrap_string(a), self.symbol, _wrap_string(b))


class _AbstractContainsComparisonOperation(_Comparison):
    def __init__(self, name):
        super(_AbstractContainsComparisonOperation, self).__init__(name=name, symbol=' CONTAINS ')


class _ContainsComparisonOperation(_AbstractContainsComparisonOperation):
    def __init__(self):
        super(_ContainsComparisonOperation, self).__init__(name='contains')


class _InComparisonOperation(_AbstractContainsComparisonOperation):
    def __init__(self):
        super(_InComparisonOperation, self).__init__(name='is in')

    def _binary(self, a, b):
        return super(_InComparisonOperation, self)._binary(b, a)


class Comparison(object):
    __equal_to = _Comparison(name=u'equal to', symbol=u'=')
    __not_equal_to = _Comparison(name=u'not equal to', symbol=u'<>')
    __greater_than = _Comparison(name=u'greater than', symbol=u'>')
    __greater_than_or_equal_to = _Comparison(name=u'greater than or equal to', symbol=u'>=')
    __less_than = _Comparison(name=u'less than', symbol=u'<')
    __less_than_or_equal_to = _Comparison(name=u'less than or equal to', symbol=u'<=')
    __is_null = _Comparison(name='null', symbol=' IS NULL', arity=Operation.UNARY)
    __is_not_null = _Comparison(name='not null', symbol=' IS NOT NULL', arity=Operation.UNARY)
    __starts_with = _Comparison(name='starts with', symbol=' STARTS WITH ')
    __ends_with = _Comparison(name='starts with', symbol=' ENDS WITH ')
    __contains = _ContainsComparisonOperation()
    __is_in = _InComparisonOperation()

    @property
    def equal_to(self):
        return self.__equal_to

    @property
    def eq(self):
        return self.equal_to

    @property
    def not_equal_to(self):
        return self.__not_equal_to

    @property
    def ne(self):
        return self.not_equal_to

    @property
    def greater_than(self):
        return self.__greater_than

    @property
    def gt(self):
        return self.greater_than

    @property
    def greater_than_or_equal_to(self):
        return self.__greater_than_or_equal_to

    @property
    def gte(self):
        return self.greater_than_or_equal_to

    @property
    def less_than(self):
        return self.__less_than

    @property
    def lt(self):
        return self.less_than

    @property
    def less_than_or_equal_to(self):
        return self.__less_than_or_equal_to

    @property
    def lte(self):
        return self.less_than_or_equal_to

    @property
    def is_null(self):
        return self.__is_null

    @property
    def z(self):
        return self.is_null

    @property
    def is_not_null(self):
        return self.__is_not_null

    @property
    def n(self):
        return self.is_not_null

    @property
    def starts_with(self):
        return self.__starts_with

    @property
    def ends_with(self):
        return self.__ends_with

    @property
    def contains(self):
        return self.__contains

    @property
    def is_in(self):
        return self.__is_in


# BOOLEAN
####################

class _Boolean(Operation):
    pass


class Boolean(object):
    pass


# STRING
####################


class _String(Operation):
    pass


class String(object):
    pass


# COLLECTION
####################
class _Collection(Operation):
    pass


class Collection(object):
    pass


# REGEX
####################


class _Regex(Operation):
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
