import pytesseract, os, shutil, pdf2image, csv, re, datetime, threading

def pdf_to_csv(output_path,file):
    # Gets the file name
    Abs_invoice_file = current_folder + "\\Invoices\\" + file  # Absolute Path to filename
    filename = os.path.splitext(file)[0]

    # Check the ext, if it is pdf = Get the Image
    ext = os.path.splitext(file)[1]
    if ext == ".pdf":
        print("Converting", filename, "into Data")
        final_output_path = output_path + '\\' + filename

        # Check for existing directory
        try:
            shutil.rmtree(final_output_path)
        except:
            pass

        # Make the directory
        os.mkdir(final_output_path)

        # Set the output directory of pdf->jpg conversion
        pdf2image.convert_from_path(Abs_invoice_file, dpi=300, output_folder=final_output_path,
                                    output_file=filename, fmt="jpeg", grayscale=True)

        # Set the absolute file path to the image (absolute file path to the image)
        name_of_image = filename + "0001-1" + ".jpg"
        Abs_image_path = final_output_path + "\\" + name_of_image

        # Set the absolute file path to the txt (absolute file path to the output)
        outfile = filename + ".txt"  # Name of the output file
        Abs_outfile_path = final_output_path + '\\' + outfile

        # jpg -> txt conversion
        data = pytesseract.image_to_string(Abs_image_path)  # in_file is the path to the image in thi case

    else:
        # Make the output directory
        final_output_path = output_path + '\\' + filename

        # Check for existing directory
        try:
            shutil.rmtree(output_path)
            shutil.rmtree(final_output_path)
        except:
            pass

        # Make the directory
        os.mkdir(output_path)
        os.mkdir(final_output_path)

        # Set the absolute file path to the txt (absolute file path to the output)
        outfile = filename + ".txt"  # Name of the output file
        Abs_outfile_path = final_output_path + '\\' + outfile
        shutil.copy(Abs_invoice_file, final_output_path)

        # jpg -> txt conversion
        data = pytesseract.image_to_string(Abs_invoice_file)  # in_file is the path to the image in this case

    with open(Abs_outfile_path, 'w') as f:
        # Convert the Image to data
        f.write(data)

    # Close the file
    f.close()

    data = data.split("\n")
    data[:] = [x for x in data if x != '']
    data[:] = [x for x in data if x != ' ']
    extraction_thread = threading.Thread(target=information_extraction, args=(filename, data,))
    extraction_thread.start()


def information_extraction(name, data):
    output_folder = current_folder + "\\Output\\"
    format_folder = current_folder + "\\Sales_Format\\"
    general_format_filename = "General_Format.csv"
    myob_format_filename = "MYOB_Format.csv"

    # General format CSV columns name field
    if os.path.isfile(format_folder + general_format_filename):
        format_path = format_folder + general_format_filename
        try:
            with open(format_path, "r") as f:
                reader = csv.reader(f)
                general_columns_field = next(reader)
        except Exception as e:
            print("Error getting General CSV Format")
            print(e)

    # General format CSV columns name field
    if os.path.isfile(format_folder + myob_format_filename):
        format_path = format_folder + myob_format_filename
        try:
            with open(format_path, "r") as f:
                reader = csv.reader(f)
                myob_columns_field = next(reader)
        except Exception as e:
            print("Error getting MYOB CSV Format")
            print(e)

    customer_name = None
    PO_number = None
    invoice_number = None
    myob_invoice_number = None
    date = None
    code = []
    memo = []
    amt = []
    gst = []
    final_amt = []
    year = None

    print("Extracting", name, "Information")

    # Information Extraction
    asterisk_flag = 0

    for j in range(len(data)):

        # Financial Information Part

        # Information Region
        if data[j].__contains__("DESCRIPTION") and data[j].__contains__("CODE"):
            asterisk_flag += 1
            j += 1

        while asterisk_flag == 1:
            if re.search(r"\bSR\b", data[j]):
                code_sep = "SR"
            elif re.search(r"\bNT\b", data[j]):
                code_sep = "NT"
            else:
                code_sep = None

            if code_sep is not None:
                data[j] = data[j].split(code_sep)
                code.append(code_sep)  # Tax Code

                if re.search(r"\bGST SALE AMOUNT\b", data[j + 1]) is None and \
                        re.search(r"\bCODE\b", data[j + 1]) is None and \
                        re.search(r"\bRATE\b", data[j + 1]) is None and \
                        (re.search(r"\bNT\b", data[j + 1]) or re.search(r"\bSR\b", data[j + 1])) is None:
                    memo.append(data[j][0].strip() + ' ' + data[j + 1].strip())  # Memo
                else:
                    memo.append(data[j][0].strip())

                amount = data[j][1].strip()

                # Regex to get the amount
                amount = re.findall("[0-9.]", amount)
                amount = ''.join(str(x) for x in amount)

                try:
                    amount = float(amount)
                except Exception as e:
                    print(e)

                # Non-GST Amount
                amt.append("${:.2f}".format(amount))  # Non-GST Amount

                if code_sep == "SR":
                    # GST Amount
                    gst.append("${:.2f}".format(float(amount) * 0.07))  # Inclusive GST Amount

                    # Inclusive GST Amount
                    final_amt.append("${:.2f}".format(float(amount) * 1.07))  # Inclusive GST Amount
                else:
                    gst.append("${:.2f}".format(float(0) * 0.07))  # Inclusive GST Amount
                    final_amt.append("${:.2f}".format(float(amount)))  # Inclusive GST Amount

            j += 1

            if re.search(r"\bCODE\b", data[j]) and re.search(r"\bRATE\b", data[j]):
                asterisk_flag += 1

        # General Information

        if asterisk_flag == 2:
            break

        else:
            # Get the name
            if data[j].__contains__("CUSTOMER:"):
                customer_name = data[j + 1].strip()

            # Get the customer PO number:
            elif data[j].__contains__("PRO-FORMA INV NUMBER:"):
                data[j + 1] = data[j + 1].split("-000")
                year = data[j + 1][0].replace("PRO-INV", "").strip()
                year = ''.join([str(s) for s in year.split() if s.isdigit()])
                year = datetime.datetime.strptime(str(year), '%Y').strftime('%y')
                PO_number = "P" + year + "-" + data[j + 1][1]

            # Get the invoice number
            elif data[j].__contains__("NUMBER :"):
                data[j] = data[j].split("NUMBER :")

                # General Invoice
                invoice_number = data[j][1].strip()

                # MYOB Invoice Number
                myob_invoice_number = invoice_number.split("-000")
                year = myob_invoice_number[0].replace("INV", "")
                year = ''.join([str(s) for s in year.split() if s.isdigit()])
                year = datetime.datetime.strptime(str(year), '%Y').strftime('%y')
                myob_invoice_number = "T" + year + "-" + myob_invoice_number[1]

            # Get the date
            elif data[j].__contains__("Date:"):

                # Need to refine
                data[j] = data[j].split("Date:")
                date = data[j][1].strip().split(" ")
                day = date[0]
                month = date[1]
                date.clear()
                date.append(day), date.append(month)

    date.append(year)
    date = ''.join(str(x) for x in date)
    date = datetime.datetime.strptime(date, '%d%B%y').strftime('%d/%m/%Y')

    # Make CSV File
    general_output_csv(output_folder, name, general_columns_field, invoice_number, date, code, memo, amt, final_amt)
    print("Finish Creating General_" + name + ".csv")
    MYOB_output_csv(output_folder, name, myob_columns_field, customer_name, PO_number, myob_invoice_number, date,
                    code, memo, amt, gst, final_amt)
    print("Finish Creating MYOB_" + name + ".csv\n")


def general_output_csv(output_folder, name, columns_field, invoice, date, code, memo, amt, final_amt):
    # Get the filename
    csv_filename = "General_" + name + ".csv"
    csv_file_path = output_folder + name + "\\" + csv_filename

    with open(csv_file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(columns_field)
        for i in range(len(memo)):
            row_data = [''] * 18  # Row data
            row_data[0] = str(invoice)  # "Journal Number"
            row_data[1] = str(date)  # "Date"
            row_data[2] = memo[i]  # "Memo"
            # row_data[3] = ''  # "Inclusive"
            # row_data[4] = ''  # "Account Number"
            # row_data[5] = ''  # "Debit Ex-Tax Amount"
            # row_data[6] = ''  # "Debit Inc-Tax Amount"
            # row_data[7] = ''  # "Credit Ex-Tax Amount"
            # row_data[8] = ''  # "Credit Inc-Tax Amount"
            # row_data[9] = ''  # "Job"
            row_data[10] = code[i]  # "Tax Code"
            row_data[11] = amt[i]  # "Non-GST Amount"
            row_data[12] = final_amt[i]  # "GST Amount"
            # row_data[13] = ''  # "Import Duty Amount"
            row_data[14] = "SGD"  # "Currency Code"
            row_data[15] = str(1)  # "Exchange Rate"
            # row_data[16] = ''  # "Allocation Memo"
            # row_data[17] = ''  # "Category"
            writer.writerow(row_data)  # Write the row
    file.close()


def MYOB_output_csv(output_folder, name, columns_field, customer, PO_number,
                    invoice, date, code, memo, amt, gst, final_amt):
    # Get the filename
    csv_filename = "MYOB_" + name + ".csv"
    csv_file_path = output_folder + name + "\\" + csv_filename

    with open(csv_file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(columns_field)
        for i in range(len(memo)):
            row_data = [''] * 54  # Row data
            row_data[0] = customer  # "Co./Last Name"
            row_data[9] = str(invoice)  # "Invoice #"
            row_data[10] = str(date)  # "Date"
            row_data[11] = PO_number  # Customer PO (To be done)
            row_data[14] = memo[i]  # "Description"
            row_data[16] = amt[i]  # "Amount"
            row_data[17] = final_amt[i]  # "Inc-Tax Amount"
            row_data[20] = "SALES;" + customer  # "Journal Memo"
            row_data[25] = code[i]  # "Tax Code"
            row_data[27] = gst[i]  # "GST Amount"
            row_data[28] = "$0.00"  # "Freight Amount"
            row_data[29] = "$0.00"  # "Inc-Tax Freight Amount"
            row_data[30] = "N-T"  # "Freight Tax Code"
            row_data[31] = "$0.00"  # "Freight Non-GST Amount"
            row_data[32] = "$0.00"  # "Freight GST Amount"
            writer.writerow(row_data)  # Write the row
    file.close()


# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # r'<full_path_to_your_tesseract_executable>'
current_folder = os.getcwd()
invoice_dir = os.listdir(current_folder + "\\Invoices")  # Directory where all the invoices pdf files is in

# Create Output Folder
output_path = current_folder + "\\Output\\"

# Check for existing directory
try:
    shutil.rmtree(output_path)
except:
    pass

os.mkdir(output_path)

# Main Processing starts here
for files in invoice_dir:
    # Main code
    conversion_thread = threading.Thread(target=pdf_to_csv,args=(output_path,files,))
    conversion_thread.start()