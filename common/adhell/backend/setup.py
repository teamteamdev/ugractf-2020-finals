import setuptools

with open("requirements.txt") as req_file:
    requirements = [
        line.split()
        for line in req_file
    ]

setuptools.setup(
    name="adhell",
    version="0.1",
    author="Nikita Sychev",
    author_email="team@teamteam.dev",
    description="ugractf/ugractf-2020-finals/adhell",
    url="https://github.com/ugractf/ugractf-2020-finals",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    package_data={
        "adhell": [
            "templates/*"
        ]
    },
    install_requires=requirements,
    python_requires=">=3.6"
)
