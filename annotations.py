from PyPDF2 import PdfFileReader
import os

annotations = ['/StrikeOut', '/Popup', '/FreeText', '/Line']


def is_annotation_present(path):

    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)
        number_of_pages = pdf.getNumPages()

        for i in range(number_of_pages):
            page = pdf.getPage(i)
            try:
                for annot in page['/Annots']:
                    if annot.getObject()['/Subtype'] in annotations:
                        return True
                return False
            except:
                return False


def are_annotations_present(files_to_read):
    annotations_present = dict()

    for file in files_to_read:
        annotations_present[os.path.basename(file)] = is_annotation_present(file)

    return annotations_present


def get_list_of_annotations(path):

    list_of_annotations = list()

    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)
        number_of_pages = pdf.getNumPages()

        for i in range(number_of_pages):
            page = pdf.getPage(i)

            try:
                for annot in page['/Annots']:
                    sub_type = annot.getObject()['/Subtype']
                    if sub_type in annotations:
                        list_of_annotations.append(str(sub_type).replace('/', '') + ' on Page ' + str(i + 1))
            finally:
                return list_of_annotations


def list_annotations_present(files_to_read):

    list_of_files_and_annotations = dict()

    for file in files_to_read:
        list_of_files_and_annotations[os.path.basename(file)] = get_list_of_annotations(file)

    return list_of_files_and_annotations