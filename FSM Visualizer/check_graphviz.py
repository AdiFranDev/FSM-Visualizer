"""Check if Graphviz is properly installed."""

import subprocess
import sys
import os
from pathlib import Path

def find_graphviz_windows():
    """Try to find Graphviz installation on Windows."""
    possible_paths = [
        r"C:\Program Files\Graphviz\bin",
        r"C:\Program Files (x86)\Graphviz\bin",
        r"C:\Program Files\Graphviz 2.38\bin",
        Path.home() / "AppData" / "Local" / "Programs" / "Graphviz" / "bin",
    ]
    
    # Also check common Chocolatey paths
    possible_paths.append(r"C:\ProgramData\chocolatey\lib\Graphviz\tools\bin")
    
    for path in possible_paths:
        dot_path = Path(path) / "dot.exe"
        if dot_path.exists():
            return str(Path(path))
    
    return None

def check_graphviz():
    """Check if Graphviz 'dot' command is available."""
    try:
        result = subprocess.run(
            ['dot', '-V'],
            capture_output=True,
            text=True,
            timeout=5
        )
        print("✓ Graphviz is installed and in PATH!")
        print(f"  Version: {result.stderr.strip()}")
        return True
    except FileNotFoundError:
        print("✗ Graphviz 'dot' command not found in PATH")
        
        # Try to find it on Windows
        if sys.platform == "win32":
            found_path = find_graphviz_windows()
            if found_path:
                print(f"\n⚠ Graphviz FOUND at: {found_path}")
                print("  But it's not in your PATH!")
                print("\nTo fix this:")
                print(f"  1. Add this to your PATH: {found_path}")
                print("  2. Or run this command in PowerShell (as Administrator):")
                print(f'     $env:Path += ";{found_path}"')
                print("  3. Then RESTART your terminal/IDE")
                print("\nOR manually add to PATH:")
                print("  1. Search for 'Environment Variables' in Windows")
                print("  2. Click 'Environment Variables'")
                print("  3. Under 'System variables', find 'Path' and click 'Edit'")
                print(f"  4. Click 'New' and add: {found_path}")
                print("  5. Click OK and restart your terminal")
                return False
        
        print("\nGraphviz is NOT installed on your system.")
        print("\nTo install:")
        print("\nWindows:")
        print("  Option 1 - Direct Download:")
        print("    1. Go to: https://graphviz.org/download/")
        print("    2. Download 'stable_windows_10_cmake_Release_x64_graphviz-install.exe'")
        print("    3. Run installer and CHECK 'Add Graphviz to PATH'")
        print("    4. Restart terminal")
        print("\n  Option 2 - Chocolatey:")
        print("    choco install graphviz")
        print("\n  Option 3 - Winget:")
        print("    winget install graphviz")
        print("\nmacOS:")
        print("  brew install graphviz")
        print("\nLinux (Ubuntu/Debian):")
        print("  sudo apt-get install graphviz")
        return False
    except subprocess.TimeoutExpired:
        print("✗ Graphviz command timed out")
        return False
    except Exception as e:
        print(f"✗ Error checking Graphviz: {e}")
        return False

def check_python_package():
    """Check if graphviz Python package is installed."""
    try:
        import graphviz
        print("✓ graphviz Python package is installed")
        print(f"  Version: {graphviz.__version__}")
        return True
    except ImportError:
        print("✗ graphviz Python package not installed")
        print("  Run: pip install graphviz")
        return False

if __name__ == "__main__":
    print("Checking Graphviz installation...")
    print("="*50)
    
    python_ok = check_python_package()
    print()
    system_ok = check_graphviz()
    
    print("\n" + "="*50)
    if python_ok and system_ok:
        print("✓ All Graphviz dependencies are ready!")
        print("\nYou can now run: python run.py")
        sys.exit(0)
    else:
        print("✗ Please fix the issues above, then run this script again")
        sys.exit(1)
