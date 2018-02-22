
"""Setup"""

from setuptools import setup

def readme():
    """Readme"""
    with open("README.md") as rhand:
        return rhand.read()

setup(name='pywebber',
      version='3.5',
      description='Common tools employed in web development',
      long_description=readme(),
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Programming Language :: Python :: 3.6',
          'License :: OSI Approved :: MIT License',
          'Intended Audience :: Developers',
          'Environment :: Web Environment',
          'Topic :: Internet :: WWW/HTTP :: Browsers',
      ],
      keywords='web crawler, lorem ipsum text generator, page indexer',
      url='https://github.com/Parousiaic/py_webber',
      download_url = 'https://github.com/Parousiaic/py_webber/archive/3.1.tar.gz',
      author='Chidi Matthew Orji',
      author_email='orjichidi95@gmail.com',
      license='MIT',
      packages=['py_webber'],
      install_requires=[
          'beautifulsoup4'
      ],
      zip_safe=False,
      test_suite='nose2.collector.collector',)
