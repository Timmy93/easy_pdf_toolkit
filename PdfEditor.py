import os
import shutil
from PyPDF2 import PdfReader, PdfWriter


class PdfEditor:

    def __init__(self):
        pass

    def count_pages(self, pdf_path):
        try:
            with open(pdf_path, "rb") as file:
                reader = PdfReader(file)
                num_pages = len(reader.pages)
                return num_pages
        except Exception as e:
            return 0

    def split_pdf(self, pdf_path):
        # Get the PDF filename without extension
        pdf_filename = os.path.basename(pdf_path)
        folder_name = os.path.splitext(pdf_filename)[0]
        # Define the desktop path
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        # Create the folder on the desktop with the PDF's name
        folder_path = os.path.join(desktop_path, folder_name)

        try:
            os.makedirs(folder_path, exist_ok=True)
            print(f"Folder created: {folder_path}")
        except Exception as e:
            print(f"Error creating folder: {e}")
            return False

        # Open the PDF file and split it into individual pages
        try:
            reader = PdfReader(pdf_path)
            num_pages = len(reader.pages)
            print(f"Total pages: {num_pages}")

            for i in range(num_pages):
                # Create a PdfWriter for each page
                writer = PdfWriter()
                writer.add_page(reader.pages[i])

                # Create a new file for each page
                output_filename = os.path.join(folder_path, f"{folder_name}_pag_{i + 1}.pdf")

                # Write the single page to a new PDF file
                with open(output_filename, "wb") as output_pdf:
                    writer.write(output_pdf)
                print(f"Page {i + 1} saved as {output_filename}")
            return folder_path

        except Exception as e:
            print(f"Error processing PDF: {e}")
            return False
