# noob-wasi - Python Dependency Confusion Finder

## Overview
**noob-wasi** is a Bash script designed to detect Python Dependency Confusion vulnerabilities by identifying unregistered or private PyPI package names from exposed Python project files.

## Features
- Automatically scrapes `.py` files from Wayback Machine and GAU
- Extracts dependencies from `site-packages`
- Checks if dependencies exist on PyPI
- Highlights potential dependency confusion vulnerabilities
- Color-coded output for better readability

## Installation
Ensure you have the required dependencies installed:
```bash
sudo apt update && sudo apt install curl wget jq
```
Install **gau** and **waybackurls**:
```bash
go install github.com/lc/gau/v2/cmd/gau@latest
go install github.com/tomnomnom/waybackurls@latest
```

## Usage
Run the script with a target domain:
```bash
./noob-wasi.sh example.com
```
The script will:
1. Fetch Python-related URLs using `waybackurls` and `gau`.
2. Extract dependencies from exposed `.py` files.
3. Check if they are available on PyPI.
4. Report unregistered/private packages that could be hijacked.

## Example Output
```
██████████████████████████████████
Checking PyPI packages in example.com
Running gau on example.com
Found 12 Python files
Found some packages, verifying on PyPI
requests - Available on PyPI
custompackage123 - Private or unregistered package found!
Potential takeover: https://pypi.org/project/custompackage123
```

## Warning
🚨 **Use this tool responsibly!** The developer assumes no liability for any misuse. Always verify findings manually.

## Created by
**Muhammad Waseem**

