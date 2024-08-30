import os
import subprocess
import sys


def create_virtualenv():
    subprocess.check_call([sys.executable, "-m", "venv", ".venv"])


def install_requirements():
    pip_path = os.path.join(".venv", "Scripts", "pip") if os.name == "nt" else os.path.join(".venv", "bin", "pip")
    subprocess.check_call([pip_path, "install", "-r", "requirements.txt"])


def check_secrets_file():
    if not os.path.exists(".streamlit/secrets.toml"):
        print("Error: .streamlit/secrets.toml not found.")
        print("Please create the file and add your API keys for Supabase.")
        sys.exit(1)


def check_streamlit_file():
    if not os.path.exists("streamlit_app.py"):
        print("Error: streamlit_app.py not found.")
        sys.exit(1)


def run_streamlit_app():
    streamlit_path = os.path.join(".venv", "Scripts", "streamlit") if os.name == "nt" else os.path.join(".venv", "bin", "streamlit")
    subprocess.check_call([streamlit_path, "run", "streamlit_app.py"])


if __name__ == "__main__":
    create_virtualenv()
    install_requirements()
    check_secrets_file()
    check_streamlit_file()
    run_streamlit_app()