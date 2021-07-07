from .cli import Parser
from .cli import Command


class test_Command(Command):
	"""
	Supports the creation of commandline argument subcommands
	with support from argparse.
	"""

	def config(self):
		"""
		Configuration of arguments
		"""
		self.subparser.add_argument(
			'-v', '--version',
			action='store_true',
			help=f"get the version of the {self.name} system")

	def run(self, args):
		"""
		Configuration of arguments
		"""

		if args.version:
			print("Version is XXX")
		else:
			print("Will not show the version!")
		return 0


class App(object):

	def __init__(self):

		self.__version__ = "0.0.0"

		self.parser = Parser(
			"macrame",
			"Assembly/C/C++ utility to build embedded systems",
			"Author: Kanelis Elias")
		Command("build", "build the SW")
		Command("run", "run a remote command")
		test_Command("test", "run a remote command")

		"""
		self.parser.add_argument(
			'-v', '--verbose',
			action='store_true',
			help='an optional argument')
		"""
		"""
		self.parser.add_argument('Path',
		metavar='path',
		type=str,
		default=cwdPath,
		help='the config filepath')

		# absFilePath = os.path.dirname(os.path.abspath(__file__))
		cwdPath = os.path.abspath(os.getcwd())

		self.parser.add_argument(
			'-d', '--directory',
			type=str,
			default=cwdPath,
			help='the config filepath')

		self.parser.add_argument(
			'-v', '--version',
			action='store_true',
			help='get the version of the build system')
		"""

		# self.parser.add_argument(
		# 	'-f',
		# 	'--file',
		# 	help='A readable file',
		# 	metavar='FILE',
		# 	type=argparse.FileType('r'),
		# 	default=None)

		# Working directory
		# wd = os.path.abspath(args.directory)

		# print(f"File:              {absFilePath}")
		# print(F"CWD:               {cwdPath}")
		# print(F"Working directory: {wd}")
		# print(F"makefile path:     {makefilePath}")
		# print()

		# command(f"make -f {makefilePath}")

		# makefilePath = os.path.join(absFilePath, "conf/make/Makefile")
		# command(f"make -f {makefilePath}")

	def run(self):
		self.parser.run()

		"""
		__version__ = "xxx"

		absFilePath = os.path.dirname(os.path.abspath(__file__))
		cwdPath = os.path.abspath(os.getcwd())

		# if subcommand is None or subcommand == "build":
		makefilePath = os.path.join(absFilePath, "conf/make/Makefile")
		command(f"make -f {makefilePath}")

		# Working directory
		wd = os.path.abspath(args.directory)

		print(f"File:              {absFilePath}")
		print(F"CWD:               {cwdPath}")
		print(F"Working directory: {wd}")
		print(F"makefile path:     {makefilePath}")
		print()

		command(f"make -f {makefilePath}")
		"""


def main():
	app = App()
	rv = app.run()
	exit(rv)


if __name__ == '__main__':
	main()
