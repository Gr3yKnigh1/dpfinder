from __future__ import annotations
from typing import Generator, Callable, Optional
import shutil

from dpfinder import DuplicateFinder


def main() -> None:
	df = DuplicateFinder(target="./images", hash_size=16)
	df.on_detection.reg(lambda i1, i2: print(f"Detected duplicates: [{i1}] to [{i2}]"))
	df.on_detection.reg(lambda i1, i2: shutil.move(i1, "./out"))
	df.find_duplicates()


if __name__ == '__main__':
	main()
