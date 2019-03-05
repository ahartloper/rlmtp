# RESSLab Material Test Processing

RESSLab Material Test Processing (`rlmtp`) contains a number of tools to post-process uniaxial coupon test data.
These tools are designed to aid with filtering stress-strain data, plotting results, synchronizing different
measurements, extracting frames from videos at specified times, and more!
A set of protocols are also provided that specify _how_ the test data should be stored, and functions are provided to
rapidly process databases that are stored according to these protocols.

## Installation

`rlmtp` is currently under testing, and is therefore a private repository - this may change at some future point.
Therefore, the best way to install `rlmtp` is by clone the repository and installing it using pip.
This is done through the following commands
```
git clone https://c4science.ch/source/rlmtp.git
cd rlmtp
pip install .
```
if you are using the https protocol with git, or
```
git clone ssh://git@c4science.ch/source/rlmtp.git
cd rlmtp
pip install .
```
if you are using ssh with git.
See https://git-scm.com/ for details on git.

The first of the above commands clones (downloads) all of the files in this repository to your computer in your current
directory.
The second command makes the current directory `rlmtp`, the one you just cloned.
The third command uses pip to install the rlmtp package in your Python distribution, making the package globally
available to the distribution.

### Installing `ffmpeg`

If you would like to use the feature in `rlmtp` of extracting frames from videos you need to install `ffmpeg` on your
system.
This means that `ffmpeg.exe` and `ffprobe.exe` are on your system's path.
`ffmpeg` is a free software, the pre-compiled binaries are available at: https://www.ffmpeg.org/download.html.

### Verifying the installation

You can verify that the installation is correct by running the tests in rlmtp/tests/unit_tests/.
All the tests are run using Nosetest prior to pushing to master.
I do my best to ensure that the tests are meaningful and cover a variety of use cases.
Finally, note that the frame extraction tests may fail since they are tested using a 3 Gb file that is not part of the
repository for obvious reasons.

## Usage

A series of examples are provided in the form of Jupyter notebooks in the examples/ directory that demonstrate the
various features of `rlmtp`.

## Contributing

Via email contact with Alex Hartloper for now if you find any bugs or would like to add some features.

## Authors

Code written and maintained by Alex Hartloper (alexander.hartloper@epfl.ch).

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.

## Acknowledgments

- Be the first!
