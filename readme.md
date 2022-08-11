# RESSLab Material Test Processing

RESSLab Material Test Processing (`rlmtp`) contains a number of tools to post-process uniaxial coupon test data.
These tools are designed to aid with downsampling stress-strain data, plotting results, synchronizing different
measurements, extracting frames from videos at specified times, and more!
A set of protocols are also provided that specify _how_ the test data should be stored, and functions are provided to
rapidly process databases that are stored according to these protocols.

## Installation

`rlmtp` is currently under testing, and is therefore a private repository - this may change at some future point.
Therefore, the best way to install `rlmtp` is by clone the repository and installing it using pip.
This is done through the following commands
```
git clone git@github.com:ahartloper/rlmtp.git
cd rlmtp
pip install .
```
if you are using ssh with git.
See https://git-scm.com/ for details on git.

The first of the above commands clones (downloads) all of the files in this repository to your computer in your current directory.
The second command makes the current directory `rlmtp`, the one you just cloned.
The third command uses pip to install the rlmtp package in your Python distribution, making the package globally available to the distribution.

### Installing `ffmpeg`

If you would like to use the feature in `rlmtp` of extracting frames from videos you need to install `ffmpeg` on your
system.
This means that `ffmpeg.exe` and `ffprobe.exe` are on your system's path.
`ffmpeg` is a free software, the pre-compiled binaries are available at: https://www.ffmpeg.org/download.html.

### Installing `polyprox`

The Python package `polyprox` is needed for the downsampler in rlmtp.
This package should be installed automatically but requires the Visual Studio build tools to compile the C code on Windows.
However, on Windows machines, you may recieve an error: `C1083: Cannot open include file: 'unistd.h'` because this header file is not included with VC++ (it's a Unix header).
This error can be fixed by creating a `unistd.h` file on the search path of MSVC (e.g., `C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\VC\Tools\MSVC\14.23.28105\include\unistd.h`) with the contents from https://stackoverflow.com/a/826027 (copy the text in the box of the stackoverflow comment).
Then comment out the line `#include <getopt.h>` (replace with `\\ #include <getopt.h>`) because it is not needed.

### Verifying the installation

You can verify that the installation is correct by running the tests in rlmtp/tests/unit_tests/.
All the tests are run using Nosetest prior to pushing to master.
I do my best to ensure that the tests are meaningful and cover a variety of use cases.
Finally, note that the frame extraction tests may fail since they are tested using a 3 Gb file that is not part of the
repository for obvious reasons.

## Usage

A series of examples are provided in the form of Jupyter notebooks in the `Examples/` directory that demonstrate the
various features of `rlmtp`.
`rlmtp` is documented using doc strings, then Doxygen is used to compile all the doc strings into an html document.
See [docs/html/index.html](./docs/html/index.html) for the html document generated by Doxygen.
Note that the doxygen files may be out of date at any given point in time.

## Contributing

Contributions can be made using GitHub's features (e.g., creating issues, pull requests, etc.).

## Authors

Code written and maintained by Alex Hartloper (alexander.hartloper@epfl.ch).

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.

## Acknowledgments

- Be the first!
