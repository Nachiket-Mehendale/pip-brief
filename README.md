# pip-brief

A wrapper for pip that shows clean, organized installation and uninstallation summaries.

## Features

- Organized output with numbered sections
- Shows installed, already satisfied, warnings, errors, and dependencies
- Removes duplicate messages
- Works with single or multiple packages
- Verbose mode for full pip output
- Simple commands

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

### Uninstall packages

```bash
pip-brief uninstall numpy
pip-brief uninstall numpy pandas
pip-brief uninstall numpy --yes
```

The `--yes` flag skips the confirmation prompt.

## Output Examples

### Single package install: