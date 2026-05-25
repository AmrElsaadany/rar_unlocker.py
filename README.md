# RAR Unlocker

A Python utility to detect and unlock password-protected or locked RAR archives by manipulating the archive lock flags.

## Overview

`rar_unlocker.py` is a command-line tool that:
- Detects the RAR archive format (RAR 4.x or RAR 5.x)
- Checks the current lock status of RAR archives
- Removes the lock attribute from RAR 4.x archives
- Provides basic support for RAR 5.x detection

## Features

- ✅ **RAR 4.x Support**: Full support for detecting and unlocking RAR 4.x archives
- ✅ **RAR 5.x Detection**: Detects RAR 5.x format with partial parsing capabilities
- ✅ **Safe Read/Write**: Non-destructive analysis with optional unlock modification
- ✅ **Easy to Use**: Simple command-line interface

## Requirements

- Python 3.x
- No external dependencies (uses only Python standard library)

## Installation

Clone the repository:
```bash
git clone https://github.com/AmrElsaadany/rar_unlocker.py.git
cd rar_unlocker.py
```

## Usage

### View Archive Status
Check if a RAR archive is locked without making changes:
```bash
python rar_unlocker.py archive.rar
```

### Unlock Archive
Remove the lock attribute from a RAR 4.x archive:
```bash
python rar_unlocker.py archive.rar --unlock
```

## How It Works

### RAR 4.x Archives
The script:
1. Reads the RAR 4.x signature (`Rar!\x1a\x07\x00`)
2. Parses the Main Header block immediately following the signature
3. Extracts header flags to determine lock status (flag bit `0x0004`)
4. Clears the lock bit if `--unlock` flag is provided

### RAR 5.x Archives
The script:
1. Detects RAR 5.x signature (`Rar!\x1a\x07\x01\x00`)
2. Provides basic format detection
3. Notes that complex flag manipulation requires VINT field parsing

## Technical Details

- **RAR 4.x Lock Flag**: Bit `0x0004` in the Main Header flags
- **RAR 4.x Signature**: `Rar!\x1a\x07\x00` (7 bytes)
- **RAR 5.x Signature**: `Rar!\x1a\x07\x01\x00` (8 bytes)

## Example Output

```
$ python rar_unlocker.py locked_archive.rar
[+] Format detected: RAR 4.x
[!] Current Status: LOCKED

$ python rar_unlocker.py locked_archive.rar --unlock
[+] Format detected: RAR 4.x
[!] Current Status: LOCKED
[+] Success: Archive lock attribute stripped down!
```

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is intended for legitimate purposes such as managing your own archives. Users are responsible for ensuring they have the right to modify archives they access with this tool.

## Contributing

Contributions are welcome! Feel free to:
- Report bugs via GitHub Issues
- Submit pull requests with improvements
- Suggest enhancements

## Author

Created by [AmrElsaadany](https://github.com/AmrElsaadany)