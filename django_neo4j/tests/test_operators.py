# coding=utf-8
from __future__ import unicode_literals

import decimal
import unittest

from django_neo4j.operator import ops, Operator
from django_neo4j.util import to_long


class OperatorTest(unittest.TestCase):
    def assertArity(self, method, arity=Operator.BINARY):
        with self.assertRaisesRegexp(ValueError, 'arity'):
            if arity == Operator.UNARY:
                method(1, 2)
            elif arity == Operator.BINARY:
                method(1)
            else:
                raise RuntimeError('unknown arity')


class MathematicalOperatorsTest(OperatorTest):
    def assertOperator(self, method, symbol, arity=Operator.BINARY):
        for a, b in (
            (1, 2),
            (1.2, 2.2),
            (to_long(1), to_long(2)),
            (decimal.Decimal('1.2'), decimal.Decimal('2.2')),
            (-1, -2),
            (-1.2, -2.2),
            (to_long(-1), to_long(-2)),
            (decimal.Decimal('-1.2'), decimal.Decimal('-2.2')),
        ):
            self.assertEquals(u'{}{}{}'.format(a, symbol, b), method(a, b))

        for a, b in (
            ('', 1),
            (1, ''),
            (complex(1), 1),
            (1, complex(1)),
            (None, 1),
            (1, None),
        ):
            with self.assertRaisesRegexp(ValueError, 'argument not of type'):
                method(a, b)

        self.assertArity(method=method, arity=arity)

    def test_add(self):
        self.assertOperator(ops.mathematical.add, '+')

    def test_subtract(self):
        self.assertOperator(ops.mathematical.subtract, '-')

    def test_multiply(self):
        self.assertOperator(ops.mathematical.multiply, '*')

    def test_divide(self):
        self.assertOperator(ops.mathematical.divide, '/')
        with self.assertRaises(ZeroDivisionError):
            ops.mathematical.divide(1, 0)

    def test_mod(self):
        self.assertOperator(ops.mathematical.mod, '%')

    def test_pow(self):
        self.assertOperator(ops.mathematical.pow, '^')
