from setuptools import setup, find_packages

setup(name='trendindex',
      version='1.0.1',
      packages=find_packages(), # include all packages under abanalysis
      description='Calculates trend and store index for AB Testing.',
      url='https://upload.pypi.org/legacy',
      author='Sarbadal Pal',
      author_email='sarbadal@gmail.com',
      license='Novus',
      package_data={'': []},
      install_requires=['pandas', 'numpy'], #external packages as dependencies
      include_package_data=True,
      zip_safe=False)