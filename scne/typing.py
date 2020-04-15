############################################################
# Copyright (c) 2020 SCNE Project.
#
# Author: urain39@qq.com
# License: MIT
# Update: 2020-04-10
############################################################

from typing import (
	Any, Callable, Generator, Pattern, Tuple, Optional
)

Position = Tuple[str, int, int]
Rule = Tuple[str, Pattern[str], Optional[Callable[[str], str]]]
Token = Tuple[str, Any, Position]
TokenGenerator = Generator[Token, None, None]
