#!/usr/bin/env python

from .utils import toString
from argparse import SUPPRESS


def complete(parser, argument=None):
	"""
	Get completion for argument given
	e.g: argument: 'build -p' -> avr, stm32

	if argument is None then show all completions

	param parser: The argument parser
	param argument: The commandline argument to parse
	"""

	# ---------------------------------------------------------------------
	# The dictionary that holds all completions
	completionDict = dict()

	def add2CompletionDict(cmd, choice):

		choice = toString(choice)

		try:
			if isinstance(completionDict[cmd], set):
				completionDict[cmd].add(choice)
		except Exception:
			completionDict[cmd] = set()
			completionDict[cmd].add(choice)

	# ---------------------------------------------------------------------
	# Main arguments

	for action in parser._positionals._actions:

		for option_string in action.option_strings:

			# Complete main arguments
			cmd = ""
			choices = option_string
			add2CompletionDict(cmd, choices)

			# Complete main argument choices
			cmd = option_string
			choices = action.choices
			add2CompletionDict(cmd, choices)

	# ---------------------------------------------------------------------
	# Subcommands

	for action in parser._get_positional_actions():

		subcommands = action._choices_actions
		for subcommand in subcommands:

			# -----------------------------------------------------
			# Complete subparsers
			cmd = ""
			choices = subcommand.dest
			add2CompletionDict(cmd, choices)

		if action.choices:
			for subparse_name in action.choices:
				subparser = action.choices[subparse_name]
				optional_actions = subparser._get_optional_actions()
				for optional_action in optional_actions:
					if optional_action.help == SUPPRESS:
						continue
					args = optional_action.option_strings

					for arg in args:
						# Subparser argument completion
						cmd = subparse_name
						choices = arg
						add2CompletionDict(cmd, choices)

						# Subparser choice completion
						cmd = f"{subparse_name} {arg}"
						choices = optional_action.choices
						add2CompletionDict(cmd, choices)

	# ---------------------------------------------------------------------
	# Prepare results to be returned
	rv = ""
	if argument is not None:

		try:
			rv = toString(completionDict[argument])
		except Exception:
			pass
	else:
		for k in completionDict:
			completion = toString(sorted(completionDict[k]))
			rv += f"{k:20} | '{completion}'\n"
	return rv
