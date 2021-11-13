from __future__ import annotations
import shutil
import argparse
import os

from dpfinder import DuplicateFinder


parser = argparse.ArgumentParser()
parser.add_argument("target", help="target directory path")
parser.add_argument("--out", help="output directory path", default=".\out")
args = parser.parse_args()


# TODO(gr3yknigh1): Make it installable (maybe `zipapp`)
def main() -> int:

	target_path = args.target
	out_path = args.out

	if not os.path.exists(target_path):
		print(f"Passed path doesn't exists!\n{target_path}")
		return 

	df = DuplicateFinder(target=target_path, hash_size=16)
	df.on_detection.reg(lambda i1, i2: print(f"Detected duplicates: [{i1}] to [{i2}]"))
	df.on_detection.reg(lambda i1, i2: shutil.move(i1, out_path))

	df.find_duplicates()

	return 0


if __name__ == '__main__':
	raise SystemExit(main())
