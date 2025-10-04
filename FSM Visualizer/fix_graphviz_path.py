"""Add Graphviz to PATH automatically."""

import os
import sys
import subprocess
from pathlib import Path

def add_to_path_windows(graphviz_path):
    """Add Graphviz to Windows PATH."""
    try:
        # Try to add to user PATH (doesn't require admin)
        current_path = os.environ.get('PATH', '')
        
        if graphviz_path in current_path:
            print("✓ Graphviz is already in PATH (current session)")
            return True
        
        # Add to current session
        os.environ['PATH'] = f"{graphviz_path};{current_path}"
        
        print(f"✓ Added to current session PATH: {graphviz_path}")
        print("\n⚠ This only works for the current terminal session!")
        print("\nTo make it permanent, run PowerShell as Administrator and execute:")
        print(f'[Environment]::SetEnvironmentVariable("Path", $env:Path + ";{graphviz_path}", [System.EnvironmentVariableTarget]::Machine)')
        print("\nOR manually:")
        print("1. Search 'Environment Variables' in Windows")
        print("2. Click 'Environment Variables'")
        print("3. Under 'System variables', find 'Path' and click 'Edit'")
        print(f"4. Click 'New' and add: {graphviz_path}")
        print("5. Click OK and restart your terminal")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def verify_dot_command():
    """Verify dot command works."""
    try:
        result = subprocess.run(['dot', '-V'], capture_output=True, text=True, timeout=5)
        print(f"\n✓ SUCCESS! Graphviz is working!")
        print(f"  {result.stderr.strip()}")
        return True
    except FileNotFoundError:
        print("\n✗ 'dot' command still not found")
        return False

if __name__ == "__main__":
    print("Fixing Graphviz PATH...")
    print("="*50)
    
    graphviz_bin = r"C:\Program Files\Graphviz\bin"
    
    if not Path(graphviz_bin).exists():
        print(f"✗ Graphviz not found at: {graphviz_bin}")
        print("\nPlease install Graphviz first:")
        print("  https://graphviz.org/download/")
        sys.exit(1)
    
    print(f"Found Graphviz at: {graphviz_bin}")
    
    if add_to_path_windows(graphviz_bin):
        print("\nVerifying...")
        if verify_dot_command():
            print("\n" + "="*50)
            print("✓ You can now run: python run.py")
            print("="*50)
        else:
            print("\n⚠ Restart your terminal for PATH changes to take effect")
            print("Then run: python check_graphviz.py")
