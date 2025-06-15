import os
import threading
from PyPDF2 import PdfReader as PyPDF2Reader

class PDFReader:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PDFReader, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.cache = {}  # path → string
        self.locks = {}  # path → threading.Lock
        self.ready = {}  # path → threading.Event
        self.global_lock = threading.Lock()

    def _init_locks(self, path):
        with self.global_lock:
            if path not in self.locks:
                self.locks[path] = threading.Lock()
                self.ready[path] = threading.Event()

    def open_pdf(self, path):
        self._init_locks(path)

        # If already cached and ready, return immediately
        if path in self.cache and self.ready[path].is_set():
            return self.cache[path]

        # Otherwise, acquire lock to safely load
        with self.locks[path]:
            if path in self.cache and self.ready[path].is_set():
                return self.cache[path]

            if not os.path.exists(path):
                raise FileNotFoundError(f"The file at {path} does not exist.")

            raw_text = ""
            reader = PyPDF2Reader(path)
            for page in reader.pages:
                raw_text += page.extract_text() or ""

            self.cache[path] = raw_text
            self.ready[path].set()
            return raw_text

    def preload_pdf(self, path):
        """Call this in background thread"""
        try:
            self.open_pdf(path)
        except Exception as e:
            print(f"[!] Error loading {path}: {e}")