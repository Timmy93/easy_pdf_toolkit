import os
import shutil
from PyPDF2 import PdfReader, PdfWriter, PdfMerger


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

    def create_dir(self, pdf_path):
        # Get the PDF filename without extension
        pdf_filename = os.path.basename(pdf_path)
        folder_name = os.path.splitext(pdf_filename)[0]
        # Define the desktop path
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        # Create the folder on the desktop with the PDF's name
        folder_path = os.path.join(desktop_path, folder_name)
        try:
            os.makedirs(folder_path, exist_ok=True)
            return folder_path
        except Exception as e:
            print(f"Error creating folder: {e}")
            return False

    def split_pdf(self, pdf_path):
        # Open the PDF file and split it into individual pages
        dir_path = self.create_dir(pdf_path)
        folder_name = os.path.splitext(os.path.basename(dir_path))[0]
        if not dir_path:
            return False
        try:
            reader = PdfReader(pdf_path)
            num_pages = len(reader.pages)

            for i in range(num_pages):
                # Create a PdfWriter for each page
                writer = PdfWriter()
                writer.add_page(reader.pages[i])

                # Create a new file for each page
                output_filename = os.path.join(dir_path, f"{folder_name}_pag_{i + 1}.pdf")

                # Write the single page to a new PDF file
                with open(output_filename, "wb") as output_pdf:
                    writer.write(output_pdf)
            return dir_path

        except Exception as e:
            print(f"Error processing PDF: {e}")
            return False

    def join_pdf(self, pdf_list):
        """Join multiple pdf in a single pdf file"""
        first_file = pdf_list[0]["path"]
        dir_path = self.create_dir(first_file)
        folder_name = os.path.splitext(os.path.basename(dir_path))[0]
        output_pdf = os.path.join(dir_path, f"{folder_name}_unito.pdf")
        if not dir_path:
            return False

        # Using the merger function to merge all files
        merger = PdfMerger()
        for pdf_info in pdf_list:
            pdf = pdf_info["path"]
            with open(pdf, 'rb') as file:
                merger.append(file)

        print("Read all pdf files")
        # Write the merged output to a new file
        with open(output_pdf, 'wb') as merged_file:
            merger.write(merged_file)

        return output_pdf
