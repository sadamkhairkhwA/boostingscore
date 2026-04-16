"""
Alias for `populate_passages` (singular name) — same behavior.
"""

from reading.management.commands.populate_passages import Command as PopulatePassagesCommand


class Command(PopulatePassagesCommand):
    pass
