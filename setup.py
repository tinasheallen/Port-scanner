from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="port-scanner",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A fast, multi-threaded port scanner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/port-scanner",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "Topic :: System :: Networking",
        "Topic :: System :: Networking :: Monitoring"
    ],
    python_requires=">=3.6",
    install_requires=[],
    entry_points={
        'console_scripts': [
            'port-scanner=port_scanner.scanner:main',
        ],
    },
)
