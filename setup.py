from __future__ import annotations
import setuptools

def get_install_requires() -> list[str]:
    with open("./requirements.txt") as f:
        raw_data = f.read()
    return raw_data.splitlines()

setuptools.setup(
    name="dpfinder",
    version="0.1.0",

    author="Akkuzin Ilya",
    author_email="gr3yknigh1@gmail.com",
    url="https://github.com/gr3yknigh1/dpfinder",

    packages=setuptools.find_packages("."),
    entry_points={
        "console_scripts": ["dpfinder = dpfinder.__main__:main"]
    },

    install_requires=get_install_requires(),
    python_requires=">=3.10"
)
