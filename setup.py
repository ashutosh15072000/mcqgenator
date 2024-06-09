from setuptools import find_packages,setup

setup(
    name='mcqgenrator',
    version='0.0.1',
    author='Ashutosh Singh',
    author_email='ashutoshs019@gmail.com',
    install_requires=["openai","langchain","streamlit","python-dotenv","PyPDF2","langchain_community"],
    packages=find_packages()
)