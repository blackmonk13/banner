import setuptools

with open("banner/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="banner",
    version="1.0.0",
    author="blackmonk13",
    description="""
    A terminal-based application to manage and display 
    ASCII art and rich-text banners, written in Textual.
    """,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/blackmonk13/banner",
    project_urls={
        "Bug Tracker": "https://github.com/blackmonk13/banner/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(
        where=".",
        include=[
            "banner",
            "banner.*"
        ]
    ),
    exclude_package_data={
        "": ["*.pyc", "*.pyo", "*.pyd", "*.so", "*.dll"],
        ".venv": ["*"],
    },
    python_requires=">=3.6",
    install_requires=[
        "aiohttp",
        "art",
        "peewee",
        "rich",
        "textual",
        "validators",
    ],
    entry_points={
        "console_scripts": [
            "banner = banner.__main__:main",
        ],
    },
)
