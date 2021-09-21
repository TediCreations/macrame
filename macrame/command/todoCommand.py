#!/usr/bin/env python

"""
Todo command
"""

from ..core.cli import Command
from ..core.utils import egrep


class TodoCommand(Command):
	"""
	Lists programmer's todos
	"""

	def config(self):
		"""
		Configuration of arguments
		"""

		# Whole words
		self.subparser.add_argument(
			'-w', '--whole_words',
			action='store_true',
			help="search only for whole words")
		# Keywords
		self.subparser.add_argument(
			'-k', '--keywords',
			default=['todo', 'bug', 'fix'],
			choices=['todo', 'bug', 'fix'],
			action='store',
			type=str,
			nargs='*',
			help="keywords to search in the project")

	def run(self, args):
		"""
		Runs the command
		"""
		keywords = args.keywords
		whole_words = args.whole_words

		rv = 0
		if len(keywords) == 0:
			self.error("Please select one or more keywords")
		else:
			for keyword in keywords:
				rv = egrep(keyword, whole_words=whole_words)

		return rv
