from setuptools import find_packages, setup


setup(
    name="ml-project",
    version="0.1.0",
    description="Starter ML pipeline project scaffold.",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    py_modules=["exception", "logger", "utils"],
    install_requires=[],
    python_requires=">=3.10",
)
