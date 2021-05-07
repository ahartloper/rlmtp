from setuptools import setup

setup(name='rlmtp',
      version='0.3.4',
      description='RESSLab tools for material coupon test post-processing',
      url='https://c4science.ch/source/rlmtp/',
      author='ahartloper',
      author_email='alexander.hartloper@epfl.ch',
      license='MIT',
      packages=['rlmtp'],
      install_requires=[
          'numpy', 'pandas>=0.24.1', 'xlrd', 'matplotlib'
      ],
      zip_safe=False)
