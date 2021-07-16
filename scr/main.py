'''
https://medium.com/@somilshah112/how-to-find-duplicate-or-similar-images-quickly-with-python-2d636af9452f
'''
from __future__ import annotations
from typing import Generator, Callable, Optional

import sys
import shutil

from duplicatefinder import DuplicateFinder


def main() -> int:
	df = DuplicateFinder(target="./assets", hash_size=16)
	df.on_detection.reg(lambda i1, i2: print(f"Detected duplicates: [{i1}] to [{i2}]"))
	df.on_detection.reg(lambda i1, i2: shutil.move(i1, "./duplicates"))
	df.find_duplicates()
	return 0


if __name__ == '__main__':
	sys.exit(main())
