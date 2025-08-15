import os
from PyPDF2 import PdfReader, PdfWriter

exit = False

while not exit:
    command = input("pycrobat> ")

    if command.lower() == "exit":
        print("Bye...")
        quit()
    elif "merge " in command.lower():
        files = command.replace("merge ", "").split(" ")
        error = None

        for file in files:
            if not os.path.isfile(file):
                error = f"'{file}' is not a valid file"
        
        if error:
            print(error)
        else:
            if len(files) > 1:
                merger = PdfWriter()

                for pdf in files:
                    pdf = pdf.replace(" ", "")
                    merger.append(pdf)

                filename = input("Write filename for merged PDFs: ")

                merger.write(filename.replace(".pdf", "") + ".pdf")
                merger.close()
                print(f"Files merged in '{filename}.pdf'")
            elif len(files) == 1:
                print("Provide 2 or more files")
            else:
                print("Files not provided")
    elif "split " in command.lower():
        command_splitted = command.replace("split ", "").split(" ")

        if len(command_splitted) == 2:
            filename = command_splitted[0]
            step = int(command_splitted[1])

            if not os.path.isfile(filename):
                print(f"'{filename}' is not a valid file")
            else:
                reader = PdfReader(filename)

                if step <= 0 or step > len(reader.pages):
                    print(f"Step '{step}' is not valid")
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
                    print("File splitted")
        else:
            print("Arguments not provided")
    elif "extract " in command.lower():
        command_splitted = command.replace("extract ", "").split(" ")
        
        if len(command_splitted) == 2:
            filename = command_splitted[0]
            pages_str = command_splitted[1]

            if not os.path.isfile(filename):
                print(f"'{filename}' is not a valid file")
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
                        print("Pages are not valid")
                    else:
                        for i in range(start, end + 1):
                            writer.add_page(reader.pages[i])

                        with open(f"{filename}{(str(start + 1))}-{str(end + 1) if start != end else start + 1}.pdf", "wb") as output:
                            writer.write(output)
        else:
            print("Arguments not provided")
    else:
        print("Invalid command")