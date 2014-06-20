#!/usr/bin/env python
# vim: ai ts=2 sts=2 et sw=2
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "thousand.settings")
    
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
