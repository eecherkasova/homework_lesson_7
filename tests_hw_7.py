import pytest
import os.path
import shutil
from io import BytesIO
from os import path
from zipfile import ZipFile
from pypdf import PdfReader
from openpyxl import load_workbook
import xlrd
from xlrd import open_workbook, Book

def test_namelist():
    newzip = ZipFile(r"Hello.zip","w")
    newzip.write(r'files/Orders.xls')
    newzip.write(r'files/receipt.pdf')
    newzip.write(r'files/swaps.csv')
    newzip.close()
    print(newzip.namelist())
    assert newzip.namelist() == ['files/Orders.xls', 'files/receipt.pdf', 'files/swaps.csv']


def test_location():
    if not os.path.exists("resourses"):
        os.mkdir("resourses")
    source_path = "Hello.zip"
    if not path.exists(source_path):
        destination_path = "resourses"
        new_location = shutil.move(source_path, destination_path)
        print("Архив перемещен в указанное место")
    else:
        print("Файл не существует.")


def test_pdf():
    with ZipFile("resourses/Hello.zip") as zip_file:
        receipt = PdfReader(BytesIO(zip_file.read("files/receipt.pdf")))
        page = receipt.pages[0]
        pdftext = page.extract_text()
        print(pdftext)
        assert "Получатель Елизавета Ч." in pdftext
        number_of_pdf_pages = len(receipt.pages)
        print(number_of_pdf_pages)
        assert number_of_pdf_pages == 1


def test_csv():
    with ZipFile("resourses/Hello.zip") as zip_file:
        swaps = zip_file.read('files/swaps.csv')
        print(swaps)
        assert swaps == b'symbol, swap_short, swap_long\r\nEURUSD,0.8928,1.11755\r\nGBPUSD,0.90675,0.4371\r\n'


#with ZipFile("resourses/Hello.zip") as zip_file:
    #with zip_file.open('files/Orders.xls') as xls_file:
        #workbook = open_workbook(xls_file)
