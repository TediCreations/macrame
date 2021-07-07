#!/usr/bin/env python3

from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))

# ------------------------------------------------------------------------------

# Package name
packageName = "macrame"

# 
about = {}
with open(path.join(here, f"{packageName}/version.py"), 'r', encoding='utf-8') as f:
	exec(f.read(), about)

# Long description
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
	long_description = f.read()

# ------------------------------------------------------------------------------
# Setup config
setup(
	use_scm_version=True,
	setup_requires=['setuptools_scm'],

	name=packageName,
	packages=[packageName],
	version=about['__version__'],
	license=about['__license__'],
	description='Build utils',
	long_description=long_description,
	long_description_content_type='text/markdown',
	author=about['__author__'],
	author_email=about['__email__'],
	url=f"https://github.com/TediCreations/{packageName}",
	download_url=f"https://github.com/TediCreations/{packageName}/archive/" + about['__version__'] + '.tar.gz',
	keywords=['build', 'make', 'util'],
	install_requires=["importlib-metadata"],
	# package_data={'alphabhta': ['conf/make/*']},
	include_package_data=True,
	entry_points={
		"console_scripts": [
			"mac = macrame.app:main",
			"macrame = macrame.app:main",
		]
	},
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Build Tools',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.6',
	],
)
