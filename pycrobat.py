"""
PyCrobat - Simone Cecire
A simple tool to manage PDFs using a CLI written in Python.
"""

import os
from PyPDF2 import PdfReader, PdfWriter

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

exit = False

while not exit:
    command = input("pycrobat> ")

    if command.lower() == "exit":
        print("Bye...")
        quit()
    elif command.lower() == "clear":
        os.system('cls')
    elif "merge " in command.lower():
        files = command.replace("merge ", "").split(" ")
        error = None
        filename = files[-1]
        files.pop(len(files) - 1)

        for file in files:
            if not os.path.isfile(file):
                error = f"'{file}' is not a valid file"
        
        if error:
            print(colors.FAIL + "Error: " + error + colors.ENDC)
        else:
            if len(files) > 1:
                merger = PdfWriter()

                for pdf in files:
                    pdf = pdf.replace(" ", "")
                    merger.append(pdf)
                filename = filename.replace(".pdf", "")

                merger.write(filename + ".pdf")
                merger.close()
                print(colors.OKBLUE + f"Files merged in '{filename}.pdf'" + colors.ENDC)
            elif len(files) == 1:
                print(colors.FAIL + "Error: Provide 2 or more files" + colors.ENDC)
            else:
                print(colors.FAIL + "Files not provided" + colors.ENDC)
    elif "split " in command.lower():
        command_splitted = command.replace("split ", "").split(" ")

        if len(command_splitted) == 2:
            filename = command_splitted[0]
            step = int(command_splitted[1])

            if not os.path.isfile(filename):
                print(colors.FAIL + "Error: " + f"'{filename}' is not a valid file" + colors.ENDC)
            else:
                reader = PdfReader(filename)

                if step <= 0 or step > len(reader.pages):
                    print(colors.FAIL + "Error: " + f"Step '{step}' is not valid" + colors.ENDC)
                else:
                    writer = PdfWriter()
                    printed = 0
                    filename = filename.replace(".pdf", "")

                    for i in range(len(reader.pages)):
                        writer.add_page(reader.pages[i])
                        
                        if (i + 1) % step == 0:
                            printed += 1
                            with open(f"{filename}{printed}.pdf", "wb") as output:
                                writer.write(output)
                            writer = PdfWriter()
                        elif (i + 1) == len(reader.pages):
                            printed += 1
                            with open(f"{filename}{printed}.pdf", "wb") as output:
                                writer.write(output)
                    print(colors.OKBLUE + "File splitted" + colors.ENDC)
        else:
            print(colors.FAIL + "Error: Arguments not provided" + colors.ENDC)
    elif "extract " in command.lower():
        command_splitted = command.replace("extract ", "").split(" ")
        
        if len(command_splitted) == 2:
            filename = command_splitted[0]
            pages_str = command_splitted[1]

            if not os.path.isfile(filename):
                print(colors.FAIL + "Error: " + f"'{filename}' is not a valid file" + colors.ENDC)
            else:
                reader = PdfReader(filename)

                pages = pages_str.split("-")
                
                if len(pages) == 1:
                    pages.append(pages[0])
                
                if len(pages) > 2:
                    print("Pages are not valid")
                else:
                    writer = PdfWriter()
                    filename = filename.replace(".pdf", "")
        
                    start = int(pages[0]) - 1
                    end = int(pages[1]) - 1 if pages[1] != '' else len(reader.pages) - 1

                    if start < 0 or end > len(reader.pages) - 1 or start > end:
                        print(colors.FAIL + "Error: Pages are not valid" + colors.ENDC)
                    else:
                        for i in range(start, end + 1):
                            writer.add_page(reader.pages[i])

                        with open(f"{filename}{(str(start + 1))}-{str(end + 1) if start != end else start + 1}.pdf", "wb") as output:
                            writer.write(output)

                        print(colors.OKBLUE + f"Page extracted and saved in '{filename}{(str(start + 1))}-{str(end + 1) if start != end else start + 1}.pdf'" + colors.ENDC)
        else:
            print(colors.FAIL + "Error: Arguments not provided" + colors.ENDC)
    elif "delete " in command.lower():
        def check_delete(pages_to_delete, doc_len):
            for i in range(len(pages_to_delete)):
                if pages_to_delete[i] > doc_len or pages_to_delete[i] < 0:
                    return False
                else:
                    for j in range(len(pages_to_delete)):
                        if pages_to_delete[i] == pages_to_delete[j] and j != i:
                            return False
            return True

        command_splitted = command.replace("delete ", "").split(" ")
        
        if len(command_splitted) == 2:
            filename = command_splitted[0]
            pages_str = command_splitted[1]

            if not os.path.isfile(filename):
                print(colors.FAIL + "Error: " + f"'{filename}' is not a valid file" + colors.ENDC)
            else:
                reader = PdfReader(filename)

                pages = pages_str.split(",")
                pages = [int(page) for page in pages]
                
                if not check_delete(pages, len(reader.pages)):
                    print(colors.FAIL + "Error: Pages are not valid" + colors.ENDC)
                else:
                    writer = PdfWriter()
                    filename = filename.replace(".pdf", "")

                    if False == True:
                        print("Pages are not valid")
                    else:
                        for i in range(len(reader.pages)):
                            if (i + 1) not in pages:
                                writer.add_page(reader.pages[i])

                        with open(f"{filename}.pdf", "wb") as output:
                            writer.write(output)
                        print(colors.OKBLUE + f"Pages '{', '.join(str(p) for p in pages)}' deleted" + colors.ENDC)
        else:
            print(colors.FAIL + "Error: Arguments not provided" + colors.ENDC)
    elif "view " in command.lower():
        command_splitted = command.replace("view ", "").split(" ")
        
        if len(command_splitted) == 1:
            filename = command_splitted[0]

            if not os.path.isfile(filename):
                print(colors.FAIL + "Error: " + f"'{filename}' is not a valid file" + colors.ENDC)
            else:
                reader = PdfReader(filename)

                for page in reader.pages:
                    print(page.extract_text())
        else:
            print(colors.FAIL + "Error: Too many arguments" + colors.ENDC)
    else:
        print(colors.FAIL + f"Error: Invalid command '{command}'" + colors.ENDC)