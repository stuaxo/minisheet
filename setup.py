from setuptools import setup, find_packages

setup(
    name = "minisheet",
    version = "0.1",
    packages = find_packages(),
    
    install_requires = [],
    include_package_data = False,

    # Include the documentation
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        #'': ['' ],
    },

    author = "",
    author_email = "",
    description = "Minisheet",
    license = "LGPL",
    keywords = "csv, spreadsheet",
    url = "http://code.google.com/p/minisheet/",

    # could also include long_description, download_url, classifiers, etc.
)
