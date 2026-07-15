from __future__ import annotations

import argparse


class DefaultHelpFormatter(argparse.HelpFormatter):
    """Show ``FOO`` instead of ``subcommand.FOO`` as the metavar.

    The builder uses dotted dest names (``subcommand.file``) so values land in
    the right nested slot; this formatter strips the dotted prefix back to the
    final segment for display only.
    """

    def _get_default_metavar_for_optional(self, action: argparse.Action) -> str:
        return action.dest.split(".")[-1].upper()

    def _get_default_metavar_for_positional(self, action: argparse.Action) -> str:
        return action.dest.split(".")[-1]
