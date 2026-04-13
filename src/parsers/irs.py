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

    @staticmethod
    def _normalize_1220_line(line):
        normalized = line.rstrip("\n")
        if not normalized.strip():
            return None
        if len(normalized) != 750:
            raise ValueError(
                f"Invalid IRS 1220 record length: expected 750, got {len(normalized)}"
            )
        return normalized

    @staticmethod
    def _to_int(value):
        value = value.strip()
        return int(value) if value else 0

    @staticmethod
    def _to_amount(value, cents=False):
        value = value.strip()
        if not value:
            return 0.0

        sign = 1
        if value[0] == "+":
            value = value[1:]
        elif value[0] == "-":
            sign = -1
            value = value[1:]

        if not value:
            return 0.0

        amount = int(value)
        if cents:
            return sign * (amount / 100)
        return sign * float(amount)

    def _first_non_zero_payment_amount(self, line):
        for start, end in [
            (54, 66),
            (66, 78),
            (78, 90),
            (90, 102),
            (102, 114),
            (114, 126),
            (126, 138),
            (138, 150),
            (150, 162),
            (162, 174),
            (174, 186),
            (186, 198),
            (198, 210),
            (210, 222),
            (222, 234),
            (234, 246),
            (246, 258),
            (258, 270),
        ]:
            raw = line[start:end].strip()
            if raw and raw.strip("0").strip("+-"):
                return self._to_amount(raw, cents=True)
        return 0.0


    def process_file(self):
        """Opens and parses the IRS file, then exports the output to CSV."""
        self._parse_file()
        self._convert_irs_records_to_csv()


    def _parse_file(self):
        lines = self._file_handler.read_lines_from_file(self._filename)
        for line in lines:
            normalized = self._normalize_1220_line(line)
            if normalized is None:
                continue

            record_type = normalized[0]
            if record_type not in self._parsers:
                raise ValueError(f"Unsupported IRS 1220 record type: {record_type}")

            parsed = self._parsers[record_type](normalized)
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
            normalized = self._normalize_1220_line(line)
            if normalized is None:
                continue

            record_type = normalized[0]

            if record_type == "A":
                current_payer = self._parse_a_record(normalized)
            elif record_type == "B":
                b_record = self._parse_b_record(normalized)
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
            "TAX YEAR": line[1:5],
            "TRANSMITTER TIN": line[6:15].strip(),
            "TRANSMITTER CONTROL CODE": line[15:20].strip(),
            "TRANSMITTER NAME": line[29:69].rstrip(),
            "CONTACT NAME": line[303:343].rstrip(),
            "CONTACT PHONE": line[343:358].strip(),
            "EMAIL": line[358:408].strip(),
        }

    def _parse_a_record(self, line):
        first_name = line[52:92].rstrip()
        second_name = line[92:132].rstrip()
        payer_name = f"{first_name} {second_name}".strip()
        return {
            "RECORD TYPE": line[0:1],
            "TAX YEAR": line[1:5],
            "PAYER TIN": line[11:20].strip(),
            "PAYER NAME": payer_name,
            "ADDRESS": line[133:173].rstrip(),
            "CITY": line[173:213].rstrip(),
            "STATE": line[213:215].strip(),
            "ZIP": line[215:224].strip(),
        }

    def _parse_b_record(self, line):
        return {
            "RECORD TYPE": line[0:1],
            "TAX YEAR": line[1:5],
            "PAYEE TIN": line[11:20].strip(),
            "NAME": line[287:327].rstrip(),
            "ADDRESS": line[367:407].rstrip(),
            "STATE": line[487:489].strip(),
            "ZIP": line[489:498].strip(),
            "AMOUNT": self._first_non_zero_payment_amount(line),
        }

    def _parse_c_record(self, line):
        return {
            "RECORD TYPE": line[0:1],
            "TOTAL RECORDS": self._to_int(line[1:9]),
            "TOTAL AMOUNT": self._to_amount(line[15:33], cents=True),
        }

    def _parse_f_record(self, line):
        return {
            "RECORD TYPE": line[0:1],
            "TOTAL A RECORDS": self._to_int(line[1:9]),
        }
