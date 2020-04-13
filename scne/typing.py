############################################################
# Copyright (c) 2020 SCNE Project.
#
# Author: urain39@qq.com
# License: MIT
# Update: 2020-04-10
############################################################

from typing import Callable, Generator, Pattern, Tuple, Union

Position = Tuple[str, int, int]
Rule = Tuple[str, Pattern[str], Union[Callable[[str], str], None]]
Token = Tuple[str, str, Position]
TokenGenerator = Generator[Token, None, None]
