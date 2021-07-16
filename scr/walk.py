from __future__ import annotations
from typing import Generator

import pathlib


def walk_files_in_dir(path: str, excluded: list[str]=None) -> Generator[str, None, None]:
	if excluded is None:
		excluded = []
	else:
		excluded = [pathlib.Path(i) for i in excluded]
		for i in excluded:
			if not i.exists():
				raise ValueError(f"You excluded not existed directory [{i.absolute()}]")

	p = pathlib.Path(path)

	if not p.exists():
		raise ValueError(f"Passed directory ['{p.absolute()}'] isn't exists")
	elif not p.is_dir():
		raise ValueError(f"Passed path ['{p.absolute()}'] isn't directory")

	dirs: list[pathlib.Path] = [p]
	walked_dirs: list[pathlib.Path] = []

	for d in dirs:
		
		if d in walked_dirs or d in excluded:
			continue

		for i in d.iterdir():
			if i.is_dir():
				dirs.append(i)
			elif i.is_file():
				yield str(i.absolute())

		walked_dirs.append(d)
