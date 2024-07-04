import subprocess

# List of required packages
required_packages = [
    'google-api-python-client', #Google API Integration 
    'pywhatkit',  # WhatsApp integration
    'requests',   # HTTP requests
    'schedule'    # Job scheduling
]

# Function to install packages
def install_packages(packages):
    for package in packages:
        subprocess.check_call(['pip', 'install', package])

if __name__ == "__main__":
    install_packages(required_packages)
    print("All required packages installed successfully.")
