from setuptools import setup

APP = ['main.py']

OPTIONS = {
    'argv_emulation': False,
    'packages': ['code', 'config'],  # Include additional Python packages
    'includes': ['code', 'config'],  # Ensure these packages are included
}
setup(
    app=APP,
    options={'py2app': OPTIONS}
)
