# coding=utf-8
import sys

IS_PYTHON_3 = sys.version_info > (3,)


def to_long(o):
    if IS_PYTHON_3:
        return o

    # noinspection PyCompatibility
    return long(o)
