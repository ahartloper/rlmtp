from setuptools import setup

setup(name='rlmtp',
      version='1.0.0',
      description='RESSLab tools for material test post-processing',
      url='https://github.com/ahartloper/rlmtp',
      author='ahartloper',
      author_email='a.hartloper@imperial.ac.uk',
      license='MIT',
      packages=['rlmtp'],
      install_requires=[
          'numpy', 'pandas>=0.24.1', 'xlrd', 'matplotlib', 'polyprox'
      ],
      zip_safe=False)
