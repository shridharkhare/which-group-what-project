import os
import subprocess
import sys


def create_virtualenv():
    subprocess.check_call([sys.executable, "-m", "venv", "venv"])


def install_requirements():
    subprocess.check_call(
        [os.path.join("venv", "Scripts", "pip"), "install", "-r", "requirements.txt"]
    )


def check_secrets_file():
    if not os.path.exists(".streamlit/secrets.toml"):
        print("Error: .streamlit/secrets.toml not found.")
        print("Please create the file and add your API keys for Supabase.")
    else:
        sys.exit(1)


def check_streamlit_file():
    if not os.path.exists("streamlit_app.py"):
        print("Error: streamlit_app.py not found.")
        sys.exit(1)


def run_streamlit_app():
    subprocess.check_call(
        [os.path.join("venv", "Scripts", "streamlit"), "run", "streamlit_app.py"]
    )


if __name__ == "__main__":
    create_virtualenv()
    install_requirements()
    check_secrets_file()
    check_streamlit_file()
    run_streamlit_app()
