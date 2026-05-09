"""
PyInstaller hook for Streamlit to fix package metadata issues.
This ensures streamlit's version information is properly included.
"""

from PyInstaller.utils.hooks import collect_data_files, copy_metadata

# Collect streamlit metadata (required for version detection)
datas = copy_metadata('streamlit')

# Also collect additional streamlit data files
datas += collect_data_files('streamlit')

# Include hidden imports that Streamlit needs
hiddenimports = [
    'streamlit.runtime.scriptrunner',
    'streamlit.elements.lib.policies',
    'streamlit.web.cli',
    'streamlit.version',
    'importlib.metadata',
]
