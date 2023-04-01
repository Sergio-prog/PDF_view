import urllib.request

import PyPDF2 as pdf
from typing import Union, Optional, BinaryIO, IO
import pathlib
import io


class PDF:
    def __init__(self, path: Union[str, pathlib.Path, IO, BinaryIO], password: str = None, url_open: bool = False):
        self.path = path
        self.password = password

        if url_open:
            req = urllib.request.Request(path, headers={'User-Agent': "Magic Browser"})
            remote_file = urllib.request.urlopen(req).read()
            self.f = io.BytesIO(remote_file)
            self.file = pdf.PdfReader(self.f, password=password)
        elif type(path) == str and not url_open:
            self.f = open(path, "rb")
            self.file = pdf.PdfReader(self.f, password=password)
        else:
            self.f = path
            self.file = pdf.PdfReader(self.f, password=password)

        self.pages = self.file.pages
        self.number_of_pages = len(self.pages)

        # Metadata
        self.metadata = self.file.metadata

        self.author = self.metadata.author
        self.creator = self.metadata.creator
        self.producer = self.metadata.producer
        self.subject = self.metadata.subject
        self.title = self.metadata.title

    def read_all_pages(self) -> dict:
        result = []
        for page in range(self.number_of_pages):
            current_page = self.pages[page]
            result.append(current_page.extract_text())
        return dict(zip(range(self.number_of_pages), result))

    def get_page_text(self, page: int = 1) -> str:
        page = self.file.pages[page - 1]
        return page.extract_text()

    def write_page(self, page: int = 1) -> None:
        page = self.file.pages[page - 1]
        return None

    def save_page_images(self, page: int = 1, path: Union[str, pathlib.Path] = None) -> None:
        if not path:
            path = ''
        page = self.file.pages[page - 1]
        count = 0
        for i in page.images:
            with open(str(count) + i.name, "wb") as f:
                f.write(i.data)
                print(str(count) + i.name)
            count += 1

        return None

    def get_page_images_bytes(self, page: int = 1) -> list:
        page = self.file.pages[page - 1]
        res = []
        for i in page.images:
            res.append(str(i.data))

        return res

    def close(self):
        self.f.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(exc_type, exc_val, exc_tb)
        self.f.close()

    def __len__(self):
        return self.number_of_pages

    def __int__(self):
        return self.number_of_pages

    def __str__(self):
        return "".join(self.read_all_pages().values())


if __name__ == '__main__':
    file = open(r"C:\Users\13579\Downloads\dummy.pdf", "rb")
    pdf = PDF(r"C:\Users\13579\Downloads\Telegram Desktop\Грокаем алгоритмы ( PDFDrive ).pdf", url_open=False)
    print(pdf.save_page_images(22))
