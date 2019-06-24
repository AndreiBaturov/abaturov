import setuptools


setuptools.setup(
    name="pycalc",
    version="1.0",
    author="Andrei Baturov",
    description="Python command-line calculator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sinbat85/abaturov.git",
    packages=("pycalc",),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Maths"
    ],
    entry_points={
        'console_scripts':
            ['pycalc = pycalc.__main__:_main']
        },
)
