from io import BytesIO

from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter

import extractor.toc


def _construct_page_id_to_page_number_map(pdf, pages=None, _result=None, _num_pages=None):
    if _result is None:
        _result = {}
    if pages is None:
        _num_pages = []
        pages = pdf.trailer["/Root"].getObject()["/Pages"].getObject()
    t = pages["/Type"]
    if t == "/Pages":
        for page in pages["/Kids"]:
            _result[page.idnum] = len(_num_pages)
            _construct_page_id_to_page_number_map(pdf, page.getObject(), _result, _num_pages)
    elif t == "/Page":
        _num_pages.append(1)
    return _result


def _recursive_extract_bookmarks(outline, map_, list_):
    if isinstance(outline, list):
        for element in outline:
            _recursive_extract_bookmarks(element, map_, list_)

    else:

        list_.append({
            extractor.toc.TITLE: outline.title,
            extractor.toc.PAGE: map_[outline.page.idnum] + 1,
        })


def extract_bookmarks(pdf_filename):
    file = open(pdf_filename, 'rb')
    pdf = PdfFileReader(file)

    map_ = _construct_page_id_to_page_number_map(pdf)
    outlines = pdf.getOutlines()
    list_ = []

    _recursive_extract_bookmarks(outlines, map_, list_)

    file.close()

    return list_


def get_num_of_pages(pdf_filename):
    file = open(pdf_filename, 'rb')
    pdf = PdfFileReader(file)
    num = pdf.getNumPages()
    file.close()
    return num


def get_pages(pdf_filename, from_, to):
    if to < from_:
        to = from_

    file = open(pdf_filename, 'rb')
    pdf = PdfFileReader(file)

    output = PdfFileWriter()

    for i in range(from_ - 1, to):
        output.addPage(pdf.getPage(i))

    stream = BytesIO()
    output.write(stream)
    data = stream.getvalue()
    file.close()
    return data
