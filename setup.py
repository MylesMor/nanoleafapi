import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nanoleafapi",
    version="2.1.0",
    author="MylesMor",
    author_email="hello@mylesmor.dev",
    description="A Python 3 wrapper for the Nanoleaf OpenAPI, " +
                 "for use when controlling the Light Panels, Canvas and Shapes (including Hexagons)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MylesMor/nanoleafapi",
    packages=setuptools.find_packages(),
    install_requires=['requests', 'sseclient'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': ['effects-builder=nanoleafapi.effects_builder:interactive_builder']
    },
    python_requires='>=3.6',
)
