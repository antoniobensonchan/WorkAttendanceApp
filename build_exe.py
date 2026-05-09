"""
Build script for packaging WorkAttendanceApp Streamlit application into Windows EXE.
Uses PyInstaller with custom hooks to fix Streamlit metadata issues.
"""
import sys
import subprocess
from pathlib import Path


def check_requirements():
    """Check if required packages are installed."""
    print("=" * 60)
    print("Checking requirements...")
    print("=" * 60)
    
    try:
        import PyInstaller
        print(f"✓ PyInstaller is installed (version {PyInstaller.__version__})")
    except ImportError:
        print("✗ PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    try:
        import streamlit
        print(f"✓ Streamlit is installed (version {streamlit.__version__})")
    except ImportError:
        print("✗ Streamlit not found!")
        sys.exit(1)
    
    print()


def create_launcher():
    """Create a temporary launcher script for Streamlit."""
    print("=" * 60)
    print("Creating temporary launcher...")
    print("=" * 60)
    
    launcher_content = '''"""Launcher for Streamlit application with error handling."""
import sys
import os
import traceback
import time

print("="*60)
print("WorkAttendanceApp - Starting...")
print("="*60)
print()

# Only show pause message if running in console mode (not --windowed)
if not getattr(sys, 'frozen', False) or '--console' in sys.argv:
    print("Press ENTER to continue, or close this window to cancel...")
    input()
    print()

try:
    print("Loading Streamlit modules...")
    from streamlit.web import cli as stcli
    print("Streamlit loaded successfully.")
    print()
    
    if __name__ == "__main__":
        # Set the path to main.py
        print("Starting Streamlit server...")
        
        # Get the directory where the executable is located
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            application_path = os.path.dirname(sys.executable)
            # For --onedir mode, files are in _internal subdirectory
            internal_path = os.path.join(application_path, '_internal')
            if os.path.exists(internal_path):
                application_path = internal_path
        else:
            # Running as script
            application_path = os.path.dirname(os.path.abspath(__file__))
        
        # Construct full path to main.py
        main_py_path = os.path.join(application_path, 'main.py')
        
        print(f"Looking for main.py at: {main_py_path}")
        if not os.path.exists(main_py_path):
            print(f"ERROR: main.py not found at {main_py_path}")
            print(f"Current directory: {os.getcwd()}")
            print(f"Files in directory: {os.listdir(application_path)}")
            input("Press ENTER to exit...")
            sys.exit(1)
        
        sys.argv = [
            "streamlit",
            "run",
            main_py_path,
            "--server.headless=true",
            "--browser.gatherUsageStats=false",
            "--global.developmentMode=false",
        ]
        print("Opening browser at http://localhost:8501")
        print()
        print("Application is running. Close this window to stop.")
        print("-"*60)
        try:
            result = stcli.main()
            print()
            print("Streamlit exited with code: " + str(result))
            print("Press ENTER to exit...")
            input()
            sys.exit(result if result else 0)
        except SystemExit as e:
            print()
            print("Streamlit system exit with code: " + str(e.code))
            print("Press ENTER to exit...")
            input()
            sys.exit(e.code if e.code is not None else 0)
except Exception as e:
    # Show detailed error message
    print()
    print("="*60)
    print("ERROR: Application failed to start!")
    print("="*60)
    print()
    print(f"Error Type: {type(e).__name__}")
    print(f"Error Message: {str(e)}")
    print()
    print("Detailed traceback:")
    print("-"*60)
    print(traceback.format_exc())
    print("-"*60)
    print()
    print("Common solutions:")
    print("1. Install Visual C++ Redistributable:")
    print("   https://aka.ms/vs/17/release/vc_redist.x64.exe")
    print()
    print("2. Check if port 8501 is already in use")
    print()
    print("3. Try running as Administrator (right-click -> Run as administrator)")
    print()
    print("4. Make sure ALL files are copied, especially the _internal folder")
    print()
    print("="*60)
    print()
    
    # Try to show a message box on Windows
    try:
        import ctypes
        error_msg = f"WorkAttendanceApp Error:\\n\\n{type(e).__name__}: {str(e)}\\n\\nSee console for details."
        ctypes.windll.user32.MessageBoxW(0, error_msg, "WorkAttendanceApp Error", 0x10)
    except:
        pass
    
    print()
    print("Window will stay open. Press ENTER to exit...")
    input()
    sys.exit(1)
'''
    
    launcher_path = Path("run_app.py")
    with open(launcher_path, 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    
    print(f"✓ Created launcher: {launcher_path}")
    print()
    return launcher_path


def get_project_files():
    """Get list of project files to include."""
    print("=" * 60)
    print("Collecting project files...")
    print("=" * 60)
    
    files_to_include = [
        'main.py',
        'database.py',
        'i18n.py',
        'style.css',
        '.streamlit/config.toml',
    ]
    
    # Check if database exists
    if Path('attendance.db').exists():
        files_to_include.append('attendance.db')
        print("  ✓ Found: attendance.db (will be included)")
    
    for file in files_to_include[:-1]:  # Exclude db from this loop
        if Path(file).exists():
            print(f"  ✓ Found: {file}")
        else:
            print(f"  ⚠ Missing: {file}")
    
    print()
    return files_to_include


def build_pyinstaller_command(files):
    """Build the PyInstaller command."""
    print("=" * 60)
    print("Building PyInstaller command...")
    print("=" * 60)
    
    project_root = Path(__file__).parent
    
    # Base command with custom hooks directory
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--name=WorkAttendanceApp",
        "--onedir",  # Folder mode for faster startup
        "--windowed",  # Hide console window
        "--clean",  # Clean cache before building
        "--noconfirm",  # Overwrite without asking
        "--additional-hooks-dir=.",  # Use custom hooks from current directory
        "--add-data=run_app.py;.",  # Add launcher
    ]
    
    # Add each file with proper path separator for Windows
    for file in files:
        file_path = Path(file)
        if file_path.exists():
            # Convert to relative path if absolute
            if file_path.is_absolute():
                src_file = str(file_path.relative_to(project_root))
            else:
                src_file = str(file_path)
            
            # For files in subdirectories, preserve structure
            if file_path.parent != Path('.'):
                dest_dir = str(file_path.parent)
            else:
                dest_dir = "."
            
            cmd.append(f"--add-data={src_file};{dest_dir}")
            print(f"  + Adding: {src_file} -> {dest_dir}")
    
    # Add the launcher
    cmd.append("--add-data=run_app.py;.")
    
    # Add hidden imports
    cmd.extend([
        "--hidden-import=streamlit",
        "--hidden-import=streamlit.web.cli",
        "--hidden-import=streamlit.runtime.scriptrunner.magic_funcs",
        "--hidden-import=pandas",
        "--hidden-import=openpyxl",
    ])
    
    # Finally, add the launcher script as the entry point
    cmd.append("run_app.py")
    
    print()
    return cmd


def run_build(cmd):
    """Run the PyInstaller build process."""
    print("=" * 60)
    print("Starting build process...")
    print("=" * 60)
    print()
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=False, cwd=Path(__file__).parent)
        
        print()
        print("=" * 60)
        print("✓ Build completed successfully!")
        print("=" * 60)
        print()
        print("📦 Your application is ready in the 'dist' folder:")
        print(f"   Location: {Path(__file__).parent / 'dist' / 'WorkAttendanceApp'}")
        print()
        print("🚀 To run the application:")
        print("   1. Navigate to: dist\\WorkAttendanceApp\\")
        print("   2. Double-click: WorkAttendanceApp.exe")
        print("   3. The app will open in your default browser at http://localhost:8501")
        print()
        print("💡 Tips:")
        print("   - The entire 'WorkAttendanceApp' folder can be moved to any location")
        print("   - All dependencies are included in the folder")
        print("   - First launch may take a few seconds")
        print()
        
        # Create a debug version with console output
        print("🔧 Creating debug version with console output...")
        debug_cmd = [arg if arg != "--windowed" else "--console" for arg in cmd]
        # Change the name for debug version
        debug_cmd_final = []
        for arg in debug_cmd:
            if arg.startswith("--name="):
                debug_cmd_final.append("--name=WorkAttendanceApp_DEBUG")
            else:
                debug_cmd_final.append(arg)
        
        subprocess.run(debug_cmd_final, check=True, capture_output=False, cwd=Path(__file__).parent)
        print("✓ Debug version created: WorkAttendanceApp_DEBUG.exe")
        print("   Use this version on other PCs to see error messages if the app doesn't start")
        print()
        
    except subprocess.CalledProcessError as e:
        print()
        print("=" * 60)
        print("✗ Build failed!")
        print("=" * 60)
        print(f"Error: {e}")
        sys.exit(1)


def cleanup(launcher_path):
    """Clean up temporary files."""
    print("=" * 60)
    print("Cleaning up temporary files...")
    print("=" * 60)
    
    # Remove temporary launcher
    if launcher_path.exists():
        launcher_path.unlink()
        print(f"✓ Removed temporary launcher: {launcher_path}")
    
    # Remove build folder
    build_folder = Path("build")
    if build_folder.exists():
        import shutil
        shutil.rmtree(build_folder)
        print("✓ Removed build folder")
    
    # Remove spec file
    spec_file = Path("WorkAttendanceApp.spec")
    if spec_file.exists():
        spec_file.unlink()
        print("✓ Removed spec file")
    
    # Remove debug spec file
    debug_spec = Path("WorkAttendanceApp_DEBUG.spec")
    if debug_spec.exists():
        debug_spec.unlink()
        print("✓ Removed debug spec file")
    
    print()


def main():
    """Main build process."""
    print()
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "Streamlit EXE Builder" + " " * 27 + "║")
    print("║" + " " * 5 + "Packaging WorkAttendanceApp" + " " * 28 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    # Step 1: Check requirements
    check_requirements()
    
    # Step 2: Create launcher
    launcher_path = create_launcher()
    
    try:
        # Step 3: Get project files
        files = get_project_files()
        
        # Step 4: Build PyInstaller command
        cmd = build_pyinstaller_command(files)
        
        # Step 5: Run build
        run_build(cmd)
        
        print("=" * 60)
        print("All done! 🎉")
        print("=" * 60)
        
    finally:
        # Step 6: Cleanup
        cleanup(launcher_path)


if __name__ == "__main__":
    main()
