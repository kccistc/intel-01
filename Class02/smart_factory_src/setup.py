import setuptools

from iotdemo import __version__ as version

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="iotdemo",
    version=version,
    author="IoT demo makers group",
    author_email="demo@d-story.net",
    description="IoT demo helper APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://d-story.net",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["opencv-python", "opencv-contrib-python", "PyQt5"],
    entry_points={
        'gui_scripts': [
            'iotdemo-motion-detector = iotdemo.tuning.motion:trampoline',
            'iotdemo-color-detector = iotdemo.tuning.color.color:main',
        ],
    },
)
