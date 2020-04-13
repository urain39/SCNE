############################################################
# Copyright (c) 2020 SCNE Project.
#
# Author: urain39@qq.com
# License: MIT
# Update: 2020-04-10
############################################################

import re
from typing import Iterable, List, cast
from .exception import (
	BaseError, TokenizerError, unexpected
)
from .typing import Rule, Token, TokenGenerator


class Tokenizer():
	def __init__(self) -> None:
		self.rules: List[Rule] = [
			# Looks like Python3 solved CR/CRLF/LF problem.
			('COMMENT', re.compile(r'[#;]([^\n]+)'), None),
			('WHITESPACE', re.compile(r'([\t ]+)'), None),
			('NEWLINE', re.compile(r'(\n)'), None),
			('OPERATOR', re.compile(r'(->|\\)'), None),
			('STRING', re.compile(r'"((?:[^"\\]|\\(?:\n|.))*)"'),
				# XXX: Quick way to unescape a string.
				lambda string: cast(str, eval('"""' + string + '"""'))),
			('COMMAND', re.compile(r'@([A-Za-z_]+[0-9A-Za-z_]*)'), None),
			('LABEL', re.compile(r'\*([^\t\n "]+)'), None),
			('WORD', re.compile(r'([^\t\n "]+)'), None)
		]

	def add_rule(self, rule: Rule) -> 'Tokenizer':
		self.rules.append(rule)
		return self

	def tokenize(self, source: str, filename: str = '') -> TokenGenerator:
		i: int = 0  # Main index
		j: int = i  # Main index's backup
		l: int = len(source)

		while i < l:
			for type_, pattern, preprocess in self.rules:
				matched = pattern.match(source, i)

				if matched:
					break

			if matched:
				j = i  # Backup line index due to `yield`
				i = matched.end(0)
				value = matched.group(1) or matched.group(0)

				if preprocess:
					value = preprocess(value)

				yield type_, value, (filename, j, i)
			else:
				unexpected((filename, i, i + 1), TokenizerError, source)
