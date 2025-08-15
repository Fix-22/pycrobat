from PyPDF2 import PdfWriter
import os

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
    else:
        print("Invalid command")