import pandas as pd

from src.file_handler import FileHandler
from src.parsers import IRSParser


class TestISR:
    def _create_irs_instance(self):
        filename = "input/irs_full.txt"
        return IRSParser(
            file_handler=FileHandler(),
            filename=filename,
        )

    def test_process_file_generated_output_matches_expected(self):
        irs = self._create_irs_instance()
        irs.process_file()

        expected_records = pd.read_csv(
            "tests/files/expected/integration/irs/output/irs_output.csv"
        )
        actual_records = pd.read_csv("output/irs_output.csv")

        pd.testing.assert_frame_equal(expected_records, actual_records)
