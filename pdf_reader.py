import re
import PyPDF2


class PDFReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_pdf(self):
        with open(self.file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        return text


class PDFDataExtractor:
    def __init__(self, text):
        self.text = text

    def extract_data(self):
        data = {}

        keys = [
            "PN", "SN", "DESCRIPTION", "LOCATION", "CONDITION", "RECEIVER#", "UOM",
            "EXP DATE", "PO", "CERT SOURCE", "REC.DATE", "MFG", "BATCH#", "DOM",
            "REMARK", "LOT#", "TAGGED BY", "Qty", "NOTES"
        ]

        pattern = re.compile(r'(' + '|'.join(keys) + r'):\s*([^\s]+)')
        matches = pattern.findall(self.text)

        for key, value in matches:
            data[key] = value.strip()

        notes_pattern = re.compile(r'NOTES:\s*(.*)', re.DOTALL)
        notes_match = notes_pattern.search(self.text)
        if notes_match:
            data["NOTES"] = notes_match.group(1).strip()

        return data


class PDFValidator:
    def __init__(self, reference_template):
        self.reference_template = reference_template

    def validate_structure(self, test_keys):
        missing_keys = self.reference_template - test_keys
        extra_keys = test_keys - self.reference_template

        report = {
            "missing_keys": list(missing_keys),
            "extra_keys": list(extra_keys),
            "is_valid": len(missing_keys) == 0 and len(extra_keys) == 0
        }

        return report