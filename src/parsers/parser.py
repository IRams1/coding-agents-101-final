import os

class Parser:
    """
    Base class for all parsers.
    Whatever needed to be shared across all parsers should be implemented here.
    This includes:
    - Common methods for parsing records (e.g., adding dashes to SSN)
    - Common attributes (e.g., file handler, record lists, etc.)
    - Common logic for processing files (e.g., reading the file, determining record types,
    """
    def __init__(self, file_handler):
        self._file_handler = file_handler
        self._file_layout_name = None
        self._record_filenames = None
        self._record_lists = {}
        self._record_types = {}

    def _add_dashes_to_ssn(self, ssn: None):
        if ssn and "-" not in ssn:
            return f"{ssn[:3]}-{ssn[3:5]}-{ssn[5:9]}"
        return ssn
