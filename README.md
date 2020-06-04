# Setup

Make sure the following prerequisites are installed:
```
pip install pyqt5 pyqt5-tools requests json
```

Also make sure you have sufficient video codecs. I recommend the [K-Lite Codec Pack](http://www.codecguide.com/), but the choice is yours.

# How to use

After setup, simply run `python player.py`.

# Troubleshoot/Known issues

* I start the script, but nothing happens
..* Apparently, thats an issue with python3 on windows. Until fixed, use python 2.7 instead
* I get the following error code: `DirectShowPlayerService::doRender: Unresolved error code 0x80040218 (IDispatch error #24)`, or similar
..* You are missing video codecs, see above
* Video is blurry/doesn't resize correctly/glitches
..* This could have various reasons, the most probable ones are either a bad internet connection or PyQt just feeling like it. Not much you can do about that, sadly...
