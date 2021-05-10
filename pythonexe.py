
import PyInstaller.__main__
import subprocess

from datetime import datetime

def convert(file):

    date = datetime.now()
    date = f'{date.year}-{date.month}-{date.day} {date.hour}{date.minute}{date.second}'

    PyInstaller.__main__.run([
        file,
        '--onefile',
    ])

