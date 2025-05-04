from setuptools import setup, find_packages

setup(
    name="brick_breaker",
    version="1.0.0",
    author="Scott Faust",
    description="A classic brick breaker game built with Pygame",
    packages=find_packages(),
    install_requires=[
        "pygame==2.5.2",
        "setuptools",
        "wheel"
    ],
    include_package_data=True,
    package_data={
        "": ["img/*", "sound/*", "settings.json", "high_score.csv"]
    },
    entry_points={
        "console_scripts": [
            "brick_breaker=main:main"
        ]
    },
)
