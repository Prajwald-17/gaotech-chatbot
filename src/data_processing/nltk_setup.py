import nltk
import os

def setup_nltk():
    """Download required NLTK data"""
    try:
        # Create nltk_data directory
        nltk_data_dir = os.path.join(os.path.expanduser('~'), 'nltk_data')
        os.makedirs(nltk_data_dir, exist_ok=True)
        
        # Download required data
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        print("NLTK data downloaded successfully")
    except Exception as e:
        print(f"NLTK setup error: {e}")

if __name__ == "__main__":
    setup_nltk()