# Adobe_Photoshop_Purge_CCR_2025
------------
Python CLI script to permanently delete all files in Adobe CameraRaw Cache2 folder

Features:

Deletes files permanently (os.remove()), not to Recycle
Interactive CLI with confirmation prompt (Rich Confirm)
Uses Rich Progress for fancy output
Logs deleted files to a log file (overwrite mode) in script directory
Normalizes and validates path to ensure it's inside Cache2 directory
Ready for PyInstaller (one-dir) deployment
