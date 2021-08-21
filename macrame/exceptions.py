#!/usr/bin/env python

class UserInputError(Exception):
	def __init__(self, msg):
		message = str(msg)
		super().__init__(message)
