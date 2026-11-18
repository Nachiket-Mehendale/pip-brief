# pip-brief

A wrapper for pip that shows clean, organized installation and uninstallation summaries.

## Features

- Organized output with numbered sections
- Install single or multiple packages
- Install from requirements files with `-r`
- Uninstall single or multiple packages
- Shows packages skipped by environment markers
- Removes duplicate messages
- Verbose mode for full pip output

## Installation

```bash
pip install pip-brief
```

## Usage

### Install packages

```bash
pip-brief install numpy
pip-brief install numpy pandas matplotlib
pip-brief install numpy --verbose
```

### Install from a requirements file

```bash
pip-brief install -r requirements.txt
pip-brief install -r D:\Test\requirements.txt
pip-brief install -r base.txt -r dev.txt
```

Nested files (`-r other.txt` inside the file), version specifiers, comments and environment markers are handled by pip. A missing file or an invalid line is reported under Errors.

### Uninstall packages

```bash
pip-brief uninstall numpy
pip-brief uninstall numpy pandas
pip-brief uninstall numpy --yes
```

Without `--yes`, pip asks for confirmation. With `--yes`, the prompt is skipped and a summary is shown.

## Output Example

```
Summary of requirements.txt installation:
=========================================

1) Installed:
termcolor (3.3.0)


2) Already Satisfied:
pyyaml (6.0.3), tqdm (4.67.1)


3) Skipped:
pywin32 (marker does not match this environment)
```

## Output Sections

Install shows the sections that apply:

1. Installed - new packages
2. Already Satisfied - packages already present
3. Skipped - packages ignored by environment markers
4. Warnings - pip warnings (cleaned)
5. Errors - installation errors
6. Dependencies - packages collected

Uninstall shows:

1. Uninstalled - removed packages
2. Errors - uninstall errors

Sections are numbered in order, and only applicable ones appear.

## Requirements

- Python 3.6+
- pip

## License

MIT License - see LICENSE file