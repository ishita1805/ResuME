# import sys
# from cx_Freeze import setup, Executable

# base = None
# if sys.platform == "win32":
#     base = "Win32GUI"

# executables = [Executable("Abkuehlzeit_HP_GUI.py", base=base)]

# packages = ["click","pyfiglet","requests","PyInquirer","selenium","bs4","chromedriver-py"]
# options = {
#     'build_exe': {
#         'packages':packages,
#     },
# }

# setup(
#     name = "resume",
#     options = options,
#     version = "1.0",
#     description = 'Build and deploy beautiful websites under 5 minuites.',
#     executables = executables
# )