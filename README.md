# Adobe_Photoshop_Purge_CCR_2025
ได้รับการพัฒนาเพื่อให้ง่ายต่อการทำความสะอาดไฟล์ขยะที่สะสมใน Adobe Photoshop 2025
----------
Python CLI script to permanently delete all files in Adobe CameraRaw Cache2 folder

Features:
1. Deletes files permanently (os.remove()), not to Recycle
2. Interactive CLI with confirmation prompt (Rich Confirm)
3. Uses Rich Progress for fancy output
4. Logs deleted files to a log file (overwrite mode) in script directory
5. Normalizes and validates path to ensure it's inside Cache2 directory
6. Ready for PyInstaller (one-dir) deployment
