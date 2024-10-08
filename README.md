# markdown-to-renpy
A drag-and-drop Python script for quickly converting a script of a markdown-formatted text file into a compatible RenPy script to minimise work for developers.

While this script aims to reduce the work required to convert a script into RenPy, it does not eliminate it. You still need to name all your labels and check the output script for errors.
This script is still in development, please report any issues.



# Usage
Your script should be saved in a text or markdown file on your local computer. Download the .py file from the repository -- drag and drop the script file on the python file, and the script will automatically generate a .rpy file with the same name. If a `characters.rpy` file is detected, it will parse through it to attempt to match speakers.

# Format and Syntax
Headers will be converted into labels, while asterisks will be replaced with opening and closing RenPy text tags. 
Empty lines will be preserved.
Advanced features such as link anchors, or bold text are not currently supported
