import sys
from itertools import islice
import os
from hurry.filesize import size
import requests

# NEW imports for robust language model setup
import nltk
import spacy


def download_file(url, filename):
    """Download a file with a simple progress bar.

    Args:
        url (str): Source URL.
        filename (str): Local file path to write.

    Returns:
        bool: True if fully downloaded, False otherwise.
    """
    try:
        # Ensure parent directory exists
        os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)

        with requests.get(url, stream=True, timeout=30) as response:
            response.raise_for_status()
            total = response.headers.get('content-length')

            if total is None:
                print('There was an error while downloading: missing content-length header.')
                return False

            total = int(total)
            downloaded = 0
            with open(filename, 'wb') as file:
                for data in response.iter_content(chunk_size=max(int(total / 1000), 1024 * 1024)):
                    if not data:
                        continue
                    downloaded += len(data)
                    file.write(data)
                    done = int(50 * downloaded / total)
                    sys.stdout.write('\r[{}{}] {}/{}'.format('█' * done, '.' * (50 - done), size(downloaded), size(total)))
                    sys.stdout.flush()
            sys.stdout.write('\n')
            print('[*] Done!')
            return True
    except requests.RequestException as e:
        sys.stdout.write('\n')
        print(f"Download failed: {e}")
        # Clean up partial file
        try:
            if os.path.exists(filename):
                os.remove(filename)
        except Exception:
            pass
        return False


def chunks(data, size):
    """Yield successive n-sized chunks (dict slices)."""
    # https://stackoverflow.com/questions/22878743/how-to-split-dictionary-into-multiple-dictionaries-fast
    iterator = iter(data)
    for _ in range(0, len(data), size):
        yield {k: data[k] for k in islice(iterator, size)}


def download_language_model(notification=True):
    """Download/ensure NLP language resources (spaCy + NLTK).

    - Ensures spaCy 'en_core_web_sm' is installed (idempotent)
    - Ensures NLTK 'punkt' and 'stopwords' are present (idempotent)
    """
    if notification:
        print_header("LANGUAGE MODEL")

    # --- spaCy model ---
    if notification:
        print("Checking spaCy model: en_core_web_sm")
    try:
        spacy.load("en_core_web_sm")
        if notification:
            print("spaCy model already present.")
    except OSError:
        if notification:
            print("spaCy model not found. Downloading 'en_core_web_sm' ...")
        try:
            from spacy.cli import download as spacy_download
            spacy_download("en_core_web_sm")
            # Verify load
            spacy.load("en_core_web_sm")
            if notification:
                print("spaCy model installed successfully.")
        except Exception as e:
            print(f"Failed to download spaCy model: {e}")
            raise

    # --- NLTK resources ---
    if notification:
        print("Ensuring NLTK resources: punkt, stopwords")
    try:
        # Idempotent: will no-op if already present
        nltk.download("punkt", quiet=True)
        nltk.download("stopwords", quiet=True)
        if notification:
            print("NLTK resources are ready.")
    except Exception as e:
        print(f"Failed to download NLTK resources: {e}")
        raise


def print_header(header):
    """Pretty header for setup/update/version messages."""
    print()
    print("# ======================================================")
    print(f"#     {header}")
    print("# ======================================================")
