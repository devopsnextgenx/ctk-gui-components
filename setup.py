from setuptools import setup, find_packages

setup(
    name="ctk-gui-components",  # Unique package name
    version="0.1.4",    # Package version
    author="Amit Kshirsagar",
    author_email="devopsnextgenx@gmail.com",
    description="A collection of custom GUI components for Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/devopsnextgenx/ctk-gui-components",
    packages=find_packages(),
    install_requires=[
        "customtkinter",
        "tkinter",
        "ttkbootstrap"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: Other/Proprietary License",
 ],
    python_requires=">=3.8",
    license="SLA",
    license_files=["LICENSE"],
)
