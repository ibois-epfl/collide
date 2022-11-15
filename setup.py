setup(
    name="collision_detection",
    version="1.0.0",
    description="A small script to detect intersect meshes and output metdata",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ibois-epfl/collide",
    author="Andrea Settimi (2022)",
    author_email="info@realpython.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    # packages=["reader"],
    include_package_data=True,
    install_requires=[
        "feedparser", "html2text", "importlib_resources", "typing"
    ],
    # entry_points={"console_scripts": ["realpython=reader.__main__:main"]},
)
