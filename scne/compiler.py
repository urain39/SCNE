############################################################
# Copyright (c) 2020 SCNE Project.
#
# Author: urain39@qq.com
# License: MIT
# Update: 2020-04-10
############################################################

from os import path
from typing import Callable, List
from .exception import CompilerError, unexpected
from .tokenizer import Tokenizer
from .typing import Token, TokenGenerator


# _tokenize's annotation same as Tokenizer.tokenize
_tokenize = Tokenizer().tokenize
_normalizepath: Callable[[str, str], str] = \
	lambda path1, path2: (
		path1 if path.isabs(path1) else
			path.join(path.dirname(path2), path1))


class Compiler():
	def preprocess(self, filename: str) -> List[Token]:
		tokens: List[Token] = []
		token_generator: TokenGenerator = _tokenize(filename)

		while True:
			try:
				token = token_generator.send(None)

				if token[0] == 'COMMENT':
					continue  # Skip comment
				elif token[0] == 'COMMAND':
					if token[1] == 'import':
						while True:
							token = token_generator.send(None)

							if token[0] == 'WHITESPACE':
								continue
							elif token[0] == 'STRING':
								break
							else:
								unexpected(token[2], CompilerError)

						tokens.extend(self.preprocess(
							_normalizepath(token[1], filename)))
						continue  # Skip append `@import "xxx"`

				tokens.append(token)
			except StopIteration:
				break

		return tokens

	def compile(self, filename: str) -> None:
		tokens: List[Token] = self.preprocess(filename)
		compiled_tokens: List[Token] = []  # Tokens

		for token in tokens:
			print(token)

		print("%s compile completed" % filename)
