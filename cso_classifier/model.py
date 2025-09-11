import os
import json
import pickle

from gensim.models import KeyedVectors

from .config import Config
from .misc import print_header, download_file


class Model:
    """ Abstraction layer for cached token→CSO map + full Word2Vec model """

    def __init__(self, load_model: bool = True, use_full_model: bool = False, silent: bool = False):
        self.silent = silent
        self.model = {}          # cached token → topics (JSON)
        self.full_model = None   # gensim KeyedVectors (preferred) or legacy pickle
        self.config = Config()

        self.embedding_size = 0
        self.word_similarity = 0.7          # similarity threshold
        self.top_amount_of_words = 10       # max similar items to return

        self.use_full_model = use_full_model

        if load_model:
            self.load_models()

    # ---------------------------------------------------------------------
    # Loaders
    # ---------------------------------------------------------------------
    def load_models(self):
        """Load cached fast model, and (optionally) the full word2vec model."""
        self.__load_cached_model()
        if self.use_full_model:
            self.__load_word2vec_model()

    # ---------------------------------------------------------------------
    # Cached model (JSON)
    # ---------------------------------------------------------------------
    def __ensure_cached_model(self):
        """Ensure the cached JSON exists; download if missing."""
        local_path = self.config.get_cached_model()
        if not os.path.exists(local_path):
            if not self.silent:
                print('[*] Beginning download of cached model from', self.config.get_cahed_model_remote_url())
            download_file(self.config.get_cahed_model_remote_url(), local_path)

    def __load_cached_model(self):
        """Load the cached token→CSO JSON model (UTF-8)."""
        self.__ensure_cached_model()
        with open(self.config.get_cached_model(), "r", encoding="utf-8") as file:
            self.model = json.load(file)
        if not self.silent:
            print("Cached model loaded.")

    def check_word_in_model(self, word: str) -> bool:
        return word in self.model

    def get_words_from_model(self, word: str):
        """Return the cached mapping for a token, or {} if missing."""
        return self.model.get(word, {})

    # ---------------------------------------------------------------------
    # Full model (Word2Vec / KeyedVectors)
    # ---------------------------------------------------------------------
    def __ensure_word2vec_model(self):
        """
        Ensure the full model file exists; download if missing.

        NOTE: Historically named “pickle” in config, but server may provide a .bin.
        We keep using the getters provided by Config.
        """
        local_path = self.config.get_model_pickle_path()
        if not os.path.exists(local_path):
            if not self.silent:
                print('[*] Beginning model download from', self.config.get_model_pickle_remote_url())
            download_file(self.config.get_model_pickle_remote_url(), local_path)

    def __try_load_as_keyedvectors(self, path: str):
        """
        Try loading with Gensim 4 KeyedVectors (preferred).
        Detect binary vs. text by extension; default to binary for .bin.
        """
        lower = path.lower()
        if lower.endswith(".bin"):
            return KeyedVectors.load_word2vec_format(path, binary=True)
        elif lower.endswith(".txt") or lower.endswith(".vec"):
            return KeyedVectors.load_word2vec_format(path, binary=False)
        else:
            # Unknown extension: try binary then text
            try:
                return KeyedVectors.load_word2vec_format(path, binary=True)
            except Exception:
                return KeyedVectors.load_word2vec_format(path, binary=False)

    def __load_word2vec_model(self):
        """
        Load the full word embedding model.

        Priority:
        1) Gensim 4 KeyedVectors (word2vec format: .bin/.txt/.vec)
        2) Legacy pickle fallback (if the file is a pickled KeyedVectors/model)
        """
        self.__ensure_word2vec_model()
        path = self.config.get_model_pickle_path()

        # Try modern load first
        try:
            kv = self.__try_load_as_keyedvectors(path)
            self.full_model = kv
            self.embedding_size = int(self.full_model.vector_size)
            if not self.silent:
                print("Word2Vec model loaded (Gensim KeyedVectors).")
            return
        except Exception as e_kv:
            # Fallback: legacy pickle
            try:
                with open(path, "rb") as fh:
                    obj = pickle.load(fh)
                if hasattr(obj, "key_to_index"):  # KeyedVectors in Gensim 4
                    self.full_model = obj
                    self.embedding_size = int(self.full_model.vector_size)
                elif hasattr(obj, "wv"):  # a full Word2Vec model; use its KeyedVectors
                    self.full_model = obj.wv
                    self.embedding_size = int(self.full_model.vector_size)
                else:
                    raise TypeError("Unsupported pickle contents for word2vec model.")
                if not self.silent:
                    print("Word2Vec model loaded (legacy pickle).")
                return
            except Exception as e_pk:
                raise RuntimeError(
                    f"Failed to load word2vec model from '{path}'.\n"
                    f"- KeyedVectors error: {e_kv}\n"
                    f"- Pickle fallback error: {e_pk}"
                )

    def check_word_in_full_model(self, word: str) -> bool:
        """
        True if the token exists in the embedding vocabulary.
        """
        if not self.use_full_model:
            raise ValueError('The full word2vec model is not loaded. Set fast_classification = False')
        if self.full_model is None:
            return False
        try:
            return word in self.full_model.key_to_index  # Gensim 4 vocab
        except AttributeError:
            return word in self.full_model

    def get_embedding_from_full_model(self, word: str):
        """
        Return the embedding vector for a token, or a zero vector if missing.
        """
        if not self.use_full_model:
            raise ValueError('The full word2vec model is not loaded. Set fast_classification = False')
        if self.full_model is None:
            return [0] * self.embedding_size
        try:
            vec = self.full_model[word]  # KeyedVectors supports __getitem__
            return vec.tolist()
        except KeyError:
            return [0] * self.embedding_size

    def get_top_similar_words_from_full_model(self, grams):
        """
        Return top similar words above self.word_similarity threshold.

        Args:
            grams (str or list[str]): positive examples for most_similar.
        Returns:
            list[tuple[str, float]]
        """
        if not self.use_full_model:
            raise ValueError('The full word2vec model is not loaded. Set fast_classification = False')
        if self.full_model is None:
            return []
        try:
            sims = self.full_model.most_similar(grams, topn=self.top_amount_of_words)
            return [(token, score) for (token, score) in sims if score >= self.word_similarity]
        except KeyError:
            return []

    def get_embedding_size(self) -> int:
        if not self.use_full_model:
            raise ValueError('The full word2vec model is not loaded. Set fast_classification = False')
        return int(self.embedding_size)

    # ---------------------------------------------------------------------
    # Setup / Update helpers (downloads)
    # ---------------------------------------------------------------------
    @staticmethod
    def setup():
        """
        Ensure both cached JSON and full model files are present (download if missing).
        """
        config = Config()
        print_header("MODELS: CACHED & WORD2VEC")

        # Cached JSON
        if not os.path.exists(config.get_cached_model()):
            print('[*] Beginning download of cached model from', config.get_cahed_model_remote_url())
            ok = download_file(config.get_cahed_model_remote_url(), config.get_cached_model())
            print("Cached model downloaded successfully." if ok else "Failed to download cached model.")
        else:
            print("Nothing to do. The cached model is already available.")

        # Full model (may be .bin or pickle)
        if not os.path.exists(config.get_model_pickle_path()):
            print('[*] Beginning download of word2vec model from', config.get_model_pickle_remote_url())
            ok = download_file(config.get_model_pickle_remote_url(), config.get_model_pickle_path())
            print("Word2Vec model downloaded successfully." if ok else "Failed to download word2vec model.")
        else:
            print("Nothing to do. The word2vec model is already available.")

    @staticmethod
    def update():
        """
        Force re-download of both models.
        """
        config = Config()
        print_header("MODELS: CACHED & WORD2VEC")
        try:
            os.remove(config.get_cached_model())
        except FileNotFoundError:
            print("Couldn't delete cached model: not found")

        try:
            os.remove(config.get_model_pickle_path())
        except FileNotFoundError:
            print("Couldn't delete word2vec model: not found")

        print("Updating the models: cached and word2vec")
        ok1 = download_file(config.get_cahed_model_remote_url(), config.get_cached_model())
        ok2 = download_file(config.get_model_pickle_remote_url(), config.get_model_pickle_path())
        if ok1 and ok2:
            print("Models downloaded successfully.")
