from setuptools import setup

setup(name='rlmtp',
      version='0.6.0',
      description='RESSLab tools for material coupon test post-processing',
      url='https://github.com/ahartloper/rlmtp',
      author='ahartloper',
      author_email='alexander.hartloper@epfl.ch',
      license='MIT',
      packages=['rlmtp'],
      install_requires=[
          'numpy', 'pandas>=0.24.1', 'xlrd', 'matplotlib', 'polyprox'
      ],
      zip_safe=False)
