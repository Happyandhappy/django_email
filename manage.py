#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vhodove.settings")

    from django.core.management import execute_from_command_line
    if (sys.argv.__len__() == 1):
        sys.argv.append('runserver')

    execute_from_command_line(sys.argv)
