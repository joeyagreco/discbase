import setuptools

pkg_vars = dict()
with open("discbase/_version.py") as f:
    exec(f.read(), pkg_vars)

package_version = pkg_vars["__version__"]
minimum_python_version_required = pkg_vars["__version_minimum_python__"]

with open("requirements.txt", "r", encoding="utf8") as reqs:
    required_packages = reqs.read().splitlines()

with open("README.md") as f:
    read_me = f.read()

setuptools.setup(
    name="discbase",
    version=package_version,
    author="Joey Greco",
    author_email="joeyagreco@gmail.com",
    description="",  # TODO
    long_description_content_type="text/markdown",
    long_description=read_me,
    license="MIT",
    url="https://github.com/joeyagreco/discbase",
    include_package_data=True,
    packages=setuptools.find_packages(exclude=("test", "docs")),
    install_requires=required_packages,
    python_requires=f">={minimum_python_version_required}",
    keywords="",  # TODO
)
