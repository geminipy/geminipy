from setuptools import setup

with open('README.md') as f:
  readme = f.read()

setup(
    name='geminipy',
    version='0.0.1',
    packages=['geminipy'],
    url='https://github.com/geminipy/geminipy',
    license='GNU GPL',
    author='Mike Marzigliano',
    zip_safe=False,
    long_description=readme,
    description='API client for Gemini',
    classifiers=[
      'Gemin exchange',
      'Cryptocurrency',
      'Cryptoexchange',
      'Topic :: Cryptocurrency',
      'Topic :: Cryptocurrency:: Digital Assets Management',
    ],
)
