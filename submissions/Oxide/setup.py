import os
import sys
import subprocess
import platform

def run_command(command, description):
    print(f"{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"{description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    if sys.version_info < (3, 7):
        print("Python 3.7 or higher is required")
        return False
    print(f"Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def check_platform():
    if platform.system() != "Windows":
        print("  Warning: Victim script is designed for Windows")
        print("   Admin interface will work on any platform")
    return True

def install_victim_dependencies():
    if not os.path.exists("v/requirements.txt"):
        print("v/requirements.txt not found")
        return False
    
    return run_command(
        f"{sys.executable} -m pip install -r v/requirements.txt",
        "Installing victim dependencies"
    )

def install_admin_dependencies():
    if not os.path.exists("admin/requirements.txt"):
        print("admin/requirements.txt not found")
        return False
    
    return run_command(
        f"{sys.executable} -m pip install -r admin/requirements.txt",
        "Installing admin dependencies"
    )

def setup_django():
    if not os.path.exists("admin/manage.py"):
        print("admin/manage.py not found")
        return False
    
    os.chdir("admin")
    
    # Run migrations
    if not run_command(f"{sys.executable} manage.py makemigrations", "Creating Django migrations"):
        os.chdir("..")
        return False
    
    if not run_command(f"{sys.executable} manage.py migrate", "Running Django migrations"):
        os.chdir("..")
        return False
    
    os.chdir("..")
    return True

def main():
    print("HackDucky Setup")
    print("=" * 50)
    
    if not check_python_version():
        sys.exit(1)
    
    if not check_platform():
        sys.exit(1)
    
    if not install_victim_dependencies():
        print("Failed to install victim dependencies")
        sys.exit(1)
    
    if not install_admin_dependencies():
        print("Failed to install admin dependencies")
        sys.exit(1)
    
    if not setup_django():
        print("Failed to setup Django")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run victim script: python main.py victim")
    print("2. Start admin interface: python main.py admin")
    print("3. Open http://localhost:8000 in your browser")
    print("\nRemember: This tool is for educational purposes only!")
    print("   Always ensure you have proper authorization before use.")

if __name__ == "__main__":
    main() 