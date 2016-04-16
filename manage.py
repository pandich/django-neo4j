#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import, unicode_literals

import os
import sys

from settings import PROJECT_ROOT

sys.path.append(os.path.abspath(os.path.join(PROJECT_ROOT, u'..')))

if __name__ == u'__main__':
    os.environ.setdefault(u'DJANGO_SETTINGS_MODULE', u'settings')
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
