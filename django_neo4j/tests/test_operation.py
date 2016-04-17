# coding=utf-8
from __future__ import unicode_literals

import decimal
import unittest

from django_neo4j.exception import OperationArgumentTypeError, OperationArityError, OperationArgumentMismatchError
from django_neo4j.operation import ops, Operation
from django_neo4j.type import NULL
from django_neo4j.util import to_long


class OperationTest(unittest.TestCase):
    def assertArity(self, method, arity=Operation.BINARY):
        with self.assertRaises(OperationArityError):
            if arity == Operation.UNARY:
                method(1, 2)
            elif arity == Operation.BINARY:
                method(1)
            else:
                raise RuntimeError('unknown arity')


class MathematicalOperationsTest(OperationTest):
    def assertOperation(self, method, symbol, arity=Operation.BINARY):
        for args in [
            [1, 2],
            [1.2, 2.2],
            [to_long(1), to_long(2)],
            [decimal.Decimal('1.2'), decimal.Decimal('2.2')],
            [-1, -2],
            [-1.2, -2.2],
            [to_long(-1), to_long(-2)],
            [decimal.Decimal('-1.2'), decimal.Decimal('-2.2')],
        ]:
            self.assertEquals(u'{}{}{}'.format(args[0], symbol, args[1]), method(*args))

        for args in [
            ['', 1],
            [1, ''],
            [complex(1), 1],
            [1, complex(1)],
            [None, 1],
            [1, None],
        ]:
            with self.assertRaises(OperationArgumentTypeError):
                method(*args)

        self.assertArity(method=method, arity=arity)

    def test_add(self):
        self.assertOperation(ops.mathematical.add, '+')

    def test_subtract(self):
        self.assertOperation(ops.mathematical.subtract, '-')

    def test_multiply(self):
        self.assertOperation(ops.mathematical.multiply, '*')

    def test_divide(self):
        self.assertOperation(ops.mathematical.divide, '/')
        with self.assertRaises(ZeroDivisionError):
            ops.mathematical.divide(1, 0)

    def test_mod(self):
        self.assertOperation(ops.mathematical.mod, '%')

    def test_pow(self):
        self.assertOperation(ops.mathematical.pow, '^')


class ComparisonOperation(OperationTest):
    def assertOperation(self, method, symbol, arity=Operation.BINARY):
        if arity == Operation.UNARY:
            for a in [
                NULL,
                'abc',
                'a',
                1,
                1.2,
                to_long(1),
                decimal.Decimal('1.2'),
            ]:
                self.assertEquals(
                    u'{}{}'.format(
                        u'"{}"'.format(a) if isinstance(a, (str, unicode)) else a,
                        symbol,
                    ),
                    method(a),
                )

            for arg in (
                complex(1),
            ):
                with self.assertRaises(OperationArgumentTypeError):
                    method(arg)

        elif arity == Operation.BINARY:
            for args in [
                ['abc', 'def'],
                [1.2, 2.2],
                [to_long(1), to_long(2)],
                [decimal.Decimal('1.2'), decimal.Decimal('2.2')],
                [-1, -2],
                [-1.2, -2.2],
                [to_long(-1), to_long(-2)],
                [decimal.Decimal('-1.2'), decimal.Decimal('-2.2')],
            ]:
                if isinstance(args[0], str) != isinstance(args[1], str):
                    with self.assertRegexpMatches(ValueError, 'numeric or string'):
                        method(*args)

                else:
                    self.assertEquals(
                        u'{}{}{}'.format(
                            u'"{}"'.format(args[0]) if isinstance(args[0], (str, unicode)) else args[0],
                            symbol,
                            u'"{}"'.format(args[1]) if isinstance(args[1], (str, unicode)) else args[1],
                        ),
                        method(*args),
                    )

            for args in (
                ['', 1],
                [1, ''],
            ):
                with self.assertRaises(OperationArgumentMismatchError):
                    method(*args)

        self.assertArity(method=method, arity=arity)

    def test_equal_to(self):
        self.assertOperation(ops.comparison.equal_to, '=')

    def test_not_equal_to(self):
        self.assertOperation(ops.comparison.not_equal_to, '<>')

    def test_greater_than(self):
        self.assertOperation(ops.comparison.greater_than, '>')

    def test_greater_than_or_equal_to(self):
        self.assertOperation(ops.comparison.greater_than_or_equal_to, '>=')

    def test_less_than(self):
        self.assertOperation(ops.comparison.less_than, '<')

    def test_less_than_or_equal_to(self):
        self.assertOperation(ops.comparison.less_than_or_equal_to, '<=')

    def test_is_null(self):
        self.assertOperation(ops.comparison.is_null, ' IS NULL', arity=Operation.UNARY)

    def test_is_not_null(self):
        self.assertOperation(ops.comparison.is_not_null, ' IS NOT NULL', arity=Operation.UNARY)

    def test_starts_with(self):
        self.assertOperation(ops.comparison.starts_with, ' STARTS WITH ')

    def test_ends_with(self):
        self.assertOperation(ops.comparison.ends_with, ' ENDS WITH ')

    def test_contains(self):
        self.assertOperation(ops.comparison.contains, ' CONTAINS ')

    def test_is_in(self):
        pass
