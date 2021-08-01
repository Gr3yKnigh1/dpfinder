from __future__ import annotations
from typing import Generator

import datetime
import pathlib

from PIL import Image
import imagehash

from event import event
from walk import walk_files_in_dir


def is_image(path: str) -> bool:
	try:
		Image.open(path)
	except IOError:
		return False
	return True


class DuplicateFinder(object):
	'''
	If you want to increase performance, try to increase 'hash_size'
	'''

	target: str
	duplicates: list[str]
	hashes: dict[str, str]
	
	hash_size: int
	on_detection: event

	def __init__(self, target: str, hash_size: int=8) -> None:
		self.target = target
		self.duplicates = []
		self.hashes = {}

		self.hash_size = hash_size
		self.on_detection = event() # Callable[[str, str], None]

	
	def find_duplicates(self) -> None:
		for file in walk_files_in_dir(path, excluded):
			if is_image(file):
				self.__handle_image(image_path)


	def __handle_image(self, path: str) -> None:
		with Image.open(path) as img:
			temp_hash = imagehash.average_hash(img, self.hash_size)
			if temp_hash in self.hashes:
				self.__handling_duplicated_image(temp_hash, path, self.hashes[temp_hash])
			else:
				self.hashes[temp_hash] = path


	def __handling_duplicated_image(self, temp_hash: str, handl_path: str, stored_path: str) -> str:
		handl_path = pathlib.Path(handl_path)
		stored_path = pathlib.Path(stored_path)

		c_t1 = datetime.datetime.fromtimestamp(handl_path.stat().st_mtime)
		c_t2 = datetime.datetime.fromtimestamp(stored_path.stat().st_mtime)

		if c_t1 < c_t2:
			self.on_detection.invoke(stored_path, handl_path)
			self.hashes[temp_hash] = handl_path
			self.duplicates.append(stored_path)
		else:
			self.on_detection.invoke(handl_path, stored_path)
			self.duplicates.append(handl_path)
