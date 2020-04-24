from setuptools import setup, find_packages

setup(
    name="controllerx",
    python_requires=">=3.6",
    package_dir={"": "apps/controllerx"},
    packages=find_packages(where="apps/controllerx"),
    py_modules=["utils", "controllerx", "version", "const"],
)
