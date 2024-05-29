from setuptools import setup

APP = ['main.py']

OPTIONS = {
    'argv_emulation': False,
    'packages': ['code', 'config', 'rumps'],  # Include additional Python packages
    'includes': ['code', 'config', 'rumps'],  # Ensure these packages are included
}
REQ_LIST = [
    "py2app>=0.28.8",
    "rumps>=0.4.0"
]
setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=REQ_LIST,
)
