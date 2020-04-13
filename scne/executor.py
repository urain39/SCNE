############################################################
# Copyright (c) 2020 SCNE Project.
#
# Author: urain39@qq.com
# License: MIT
# Update: 2020-04-10
############################################################

from os import path
from typing import Callable, List
from .exception import ExecutorError, unexpected
from .tokenizer import Tokenizer
from .typing import Token, TokenGenerator


# _tokenize's annotation same as Tokenizer.tokenize
_tokenize = Tokenizer().tokenize
_normalizepath: Callable[[str, str], str] = \
	lambda path1, path2: (
		path2 if path2[0] == '/' else
			path.join(path.dirname(path1), path2))


class Executor():
	def __init__(self) -> None:
		pass

	def preprocess(self, filename: str) -> List[Token]:
		source: str = ''
		tokens: List[Token] = []
		token_generator: TokenGenerator

		try:
			with open(filename, 'r') as f:
				source = f.read()
		except FileNotFoundError as e:
			raise ExecutorError('Cannot open file \'%s\'' % filename)

		token_generator = _tokenize(source, filename)

		while True:
			try:
				token = token_generator.send(None)

				if token[0] == 'COMMAND':
					if token[1] == 'import':
						while True:
							token2 = token_generator.send(None)

							if token2[0] == 'WHITESPACE':
								continue
							elif token2[0] == 'NEWLINE':
								unexpected(token2[2],
									ExecutorError, source)
							elif token2[0] == 'STRING':
								break

						tokens.extend(self.preprocess(
							_normalizepath(filename, token2[1])))
						continue  # Skip append `@import "xxx"`

				tokens.append(token)
			except StopIteration:
				break

		return tokens

	def execute(self, filename: str = 'main.sto') -> None:
		tokens: List[Token] = self.preprocess(filename)

		for token in tokens:
			print(token)
		# TODO: 从这里开始正式译码执行。
