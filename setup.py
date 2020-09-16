from pathlib import Path
import re

from setuptools import setup

root = Path(__file__).parent

requirements = (
    (root / "requirements.txt").read_text("utf-8").strip().splitlines()
)

text = (root / "gd" / "graph" / "__init__.py").read_text("utf-8")

result = re.search(
    r"^__version__\s*=\s*[\"']([^\"']*)[\"']", text, re.MULTILINE
)

if result is None:
    raise RuntimeError("Failed to find version.")

version = result.group(1)

readme = (root / "README.rst").read_text("utf-8")


setup(
    name="gd.graph",
    author="NeKitDS",
    author_email="gdpy13@gmail.com",
    url="https://github.com/NeKitDS/gd.graph",
    project_urls={
        "Issue tracker": "https://github.com/NeKitDS/gd.graph/issues"
    },
    version=version,
    packages=["gd", "gd.graph"],
    license="MIT",
    description="Plotting Graphs in Geometry Dash.",
    long_description=readme,
    long_description_content_type="text/x-rst",
    install_requires=requirements,
    include_package_data=True,
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Natural Language :: English",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": ["gd.graph = gd.graph.__main__:main"]},
)
