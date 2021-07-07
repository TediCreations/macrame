import subprocess


def run_command(cmd):
	"""
	Run a shell command
	"""

	subprocess.call(cmd, shell=True)

	"""
	cmd_split = cmd.split()

	process = subprocess.Popen(cmd_split,
		shell=True,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE,
	universal_newlines=True)
	stdout, stderr = process.communicate()

	return stdout, stderr
	"""
