from setuptools import setup

with open('README.md') as f:
  readme = f.read()

setup(
    name='geminipy',
    version='0.0.2',
    packages=['geminipy'],
    url='https://github.com/geminipy/geminipy',
    license='GNU GPL',
    author='Mike Marzigliano',
    author_email='marzig76@gmail.com',
    zip_safe=False,
    long_description=readme,
    description='API client for Gemini',
)
