from pdf_reader import PDFReader, PDFDataExtractor, PDFValidator


def create_reference_template(file_path):
    pdf_reader = PDFReader(file_path)
    pdf_text = pdf_reader.read_pdf()

    data_extractor = PDFDataExtractor(pdf_text)
    data = data_extractor.extract_data()

    return set(data.keys())


def process_pdf(file_path):
    pdf_reader = PDFReader(file_path)
    pdf_text = pdf_reader.read_pdf()

    data_extractor = PDFDataExtractor(pdf_text)
    data = data_extractor.extract_data()

    return data


if __name__ == "__main__":
    reference_file = "test_task.pdf"

    reference_template = create_reference_template(reference_file)
    print("Эталонный шаблон:", reference_template)

    test_file = "test_file.pdf"

    validator = PDFValidator(reference_template)

    test_data = process_pdf(test_file)
    test_keys = set(test_data.keys())

    validation_report = validator.validate_structure(test_keys)

    print("Отчет о проверке:")
    print("Отсутствующие ключи:", validation_report["missing_keys"])
    print("Лишние ключи:", validation_report["extra_keys"])
    print("Соответствует ли структура эталону:", validation_report["is_valid"])