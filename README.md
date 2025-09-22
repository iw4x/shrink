# iw4x-shrink

This script is used to reduce the size of an IW4x installation for dedicated server use. It does this by removing visual assets, and the final result should be ~7GiB in size.

The result of this script will be a copy of the game that isn't usable for normal gameplay- this script is intended for server hosts only.

# Usage

1. Download the script
2. Place the script in your MW2 directory
3. Run the script

If you don't want to copy the script to your MW2 directory, you may specify it directly as an argument:

```
python3 shrink.py /path/to/"Call of Duty Modern Warfare 2"
```

This script is portable, and will run on both Windows and Linux, and depends only on Python 3 and its standard utilities.
