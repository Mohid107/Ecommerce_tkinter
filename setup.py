from setuptools import setup, find_packages

setup(
    name="ShopEasy",
    version="1.0.0",
    description="A Tkinter-based E-Commerce Application",
    author="ShopEasy Team",
    packages=find_packages(),
    install_requires=[
        "pyodbc",
        "Pillow",
        "requests",
    ],
    entry_points={
        'console_scripts': [
            'shopeasy=run:main',
        ],
    },
)
