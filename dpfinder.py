from __future__ import annotations
import os
import os.path
import argparse
import pathlib

from PIL import Image
import imagehash


def walk_files_in_dir(
    path: str, excluded: list[str] = None
) -> Generator[str, None, None]:
    if excluded is None:
        excluded = []
    else:
        excluded = [pathlib.Path(i) for i in excluded]
        for i in excluded:
            if not i.exists():
                raise ValueError(f"You excluded not existed directory [{i.absolute()}]")

    path = pathlib.Path(path)

    if not path.exists():
        raise ValueError(f"Passed directory ['{path.absolute()}'] isn't exists")
    elif not path.is_dir():
        raise ValueError(f"Passed path ['{path.absolute()}'] isn't directory")

    directories: list[pathlib.Path] = [path]
    walked_dirs: list[pathlib.Path] = []

    for directory in directories:

        if directory in walked_dirs or directory in excluded:
            continue

        for i in directory.iterdir():
            if i.is_dir():
                directories.append(i)
            elif i.is_file():
                yield str(i.absolute())

        walked_dirs.append(directory)


def is_image(path: str) -> bool:
    try:
        Image.open(path)
    except IOError:
        return False
    return True


def find_duplicates(path: str) -> Generator[None, None, tuple[str, str]]:
    for image_path in [
        file_path for file_path in walk_files_in_dir(target) if is_image(file_path)
    ]:
        with Image.open(image_path) as img:
            temp_hash = imagehash.average_hash(img, self.hash_size)
            if temp_hash in self.hashes:
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
            else:
                self.hashes[temp_hash] = image_path


def main() -> int:

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--target-directory",
        help="target directory path",
        default=".",
        dest="target_directory",
    )
    parser.add_argument(
        "-o",
        "--dup-directory",
        help="duplicate directory path",
        default="dup",
        dest="dup_directory",
    )
    parser.add_argument(
        "-h", "--hash-size", help="size of image hash", default=16, dest="hash_size"
    )
    args = parser.parse_args()

    target_directory = args.target_directory
    dup_directory = args.dup_directory
    hash_size = args.hash_size

    if not os.path.exists(target_directory):
        print(f"Path doesn't exists! '{target_directory}'")
        return 1

    duplicate_finder = DuplicateFinder(target=target_directory, hash_size=hash_size)
    duplicate_finder.on_detection.reg(
        lambda i1, i2: print(f"Detected duplicates: [{i1}] to [{i2}]")
    )
    # duplicate_finder.on_detection.reg(lambda i1, i2: shutil.move(i1, out_directory))
    duplicate_finder.find_duplicates()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
