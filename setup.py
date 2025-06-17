from setuptools import setup, find_packages

setup(
    name="DentalCRM",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # Add your project dependencies here, for example:
        # "Django>=3.2",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="Dental CRM project",
    url="https://your.project.url",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
