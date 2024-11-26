# setup.py

from setuptools import setup, find_packages

setup(
    name="device_sdk",
    version="0.1.0",
    description="A WebSocket SDK to connect devices to brain-link scanhub.",
    author="",
    author_email="",
    packages=find_packages(),
    install_requires=[
        "websockets>=10.4",
    ],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)