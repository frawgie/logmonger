from setuptools import setup

setup(
        name="logmonger",
        version="0.1.0",
        description="Logging handler with MongoDB as backend.",
        author="Jonas Ericsson",
        author_email="jonas@agilefrog.se",
        url="http://github.com/frawgie/logmonger",
        packages=["logmonger"],
        install_requires=["pymongo"],
        test_suite="nose.collector")
