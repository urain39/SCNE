############################################################
# Copyright (c) 2020 SCNE Project.
#
# Author: urain39@qq.com
# License: MIT
# Update: 2020-04-10
############################################################

from typing import NoReturn, Optional, Type
from .typing import Position, Token


class BaseError(Exception):
	pass


class ExecutorError(BaseError):
	pass


class TokenizerError(ExecutorError):
	pass


def unexpected(position: Position,
		exception_type: Type[BaseError],
		source: Optional[str] = None) -> NoReturn:
		i: int
		j: int
		k: int  # Free index

		lineno: int

		# Get token position
		filename, i, j = position

		if not source:
			with open(filename) as f:
				source = f.read()

		# Count <newline> for token info
		lineno = source.count('\n', 0, i) + 1

		# Find out nearest <newline> to calculate line index
		k = source.rfind('\n', 0, i)

		raise exception_type(
			'%s:%d:%d: Unexpected \'%s\'' % (
			filename, lineno, i - k, source[i:j]
		))
