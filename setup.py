from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="dsm_core",
    version="0.1.0",
    description="A compact 2D plane-frame Direct Stiffness Method solver "
                "(Theory of 1st/2nd Order, linear buckling analysis).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Johannes Stuempfl",
    url="https://github.com/johannesstuempfl/dsm-core",
    packages=find_packages(),
    package_dir={"": "."},
    install_requires=[
        "numpy",
    ],
    python_requires=">=3.8",
    zip_safe=False,
)
