import logging
import pandas as pd

from src.parsers.parser import Parser


class IRSParser(Parser):
    def __init__(
        self,
        file_handler,
        filename,
        *args,
        **kwargs,
    ):
        super().__init__(file_handler)
        self._filename = filename

        self._record_lists = {
            "T": [],
            "A": [],
            "B": [],
            "C": [],
            "F": [],
        }

        self._parsers = {
            "T": self._parse_t_record,
            "A": self._parse_a_record,
            "B": self._parse_b_record,
            "C": self._parse_c_record,
            "F": self._parse_f_record,
        }


    def process_file(self):
        """Opens and parses the IRS file, then exports the output to CSV."""
        self._parse_file()
        self._convert_irs_records_to_csv()


    def _parse_file(self):
        lines = self._file_handler.read_lines_from_file(self._filename)
        for line in lines:
            record_type = line[0]
            if record_type in self._parsers:
                parsed = self._parsers[record_type](line)
                self._record_lists[record_type].append(parsed)

    # ---------------- Participant Records ---------------- #
    def _convert_irs_records_to_csv(self):

        logging.info("Building IRS 1220 CSV output")

        if not self._record_lists["B"]:
            logging.warning("No B records found. Skipping CSV generation.")
            return

        enriched_rows = []
        current_payer = None

        lines = self._file_handler.read_lines_from_file(self._filename)

        for line in lines:
            record_type = line[0]

            if record_type == "A":
                current_payer = self._parse_a_record(line)
            elif record_type == "B":
                b_record = self._parse_b_record(line)
                # merge manual (contextual)
                combined = {
                    **b_record,
                    "PAYER_NAME": current_payer.get("PAYER NAME") if current_payer else None,
                    "PAYER_TIN": current_payer.get("PAYER TIN") if current_payer else None,
                }
                enriched_rows.append(combined)

        final_df = pd.DataFrame(enriched_rows)
        final_df.to_csv("output/irs_output.csv", index=False)
        logging.info(f"CSV generado con {len(final_df)} registros")

    # ---------------- Parse functions ---------------- #
    def _parse_t_record(self, line):
        return {
            "RECORD TYPE": line[0:1],
            "TRANSMITTER CONTROL CODE": line[1:10].strip(),
            "TAX YEAR": line[10:14],
            "TRANSMITTER NAME": line[14:44].rstrip(),
            "CONTACT NAME": line[44:64].rstrip(),
            "CONTACT PHONE": line[64:74].strip(),
            "EMAIL": line[74:114].strip(),
        }

    def _parse_a_record(self, line):
        line = line.rstrip("\n")

        return {
            "RECORD TYPE": line[0:1],
            "SEQUENCE NUMBER": line[1:10].lstrip(),
            "TAX YEAR": line[10:14],
            "PAYER TIN": line[14:23].strip(),
            "PAYER NAME": line[23:44].rstrip(),
            "ADDRESS": line[44:67].rstrip(),
            "STATE": line[67:69],
            "ZIP": line[71:76],
        }

    def _parse_b_record(self, line):
        line = line.rstrip("\n")
        amount_text = line[67:77].strip() or line[-10:].strip()
        return {
            "RECORD TYPE": line[0:1],
            "TAX YEAR": line[1:5],
            "PAYEE TIN": line[5:16].strip(),
            "NAME": line[16:36].rstrip(),
            "ADDRESS": line[36:57].rstrip(),
            "STATE": line[57:59],
            "ZIP": line[61:66],
            "AMOUNT": float(amount_text),
        }

    def _parse_c_record(self, line):
        return {
            "RECORD TYPE": line[0:1],
            "TOTAL RECORDS": int(line[1:9]),
            "TOTAL AMOUNT": float(line[9:21]),
        }

    def _parse_f_record(self, line):
        return {
            "RECORD TYPE": line[0:1],
            "TOTAL A RECORDS": int(line[1:9]),
        }