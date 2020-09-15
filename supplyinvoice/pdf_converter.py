import multiprocessing
from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
from PIL import ImageFilter

def pdf_to_image(img_path):
    images = convert_from_path(img_path, 
	dpi=300,  #650 for Fuji Xerox, testing filters with 300 first
	fmt='jpg', 
	grayscale=True, 
	thread_count=multiprocessing.cpu_count())
    img_path = img_path.replace(".pdf","")
    # ima_path = img_path.replace("\media","\image") 
    
    img_name_list =[]
    i = 1
    for image in images:
        # white = image.filter(ImageFilter.BLUR).filter(ImageFilter.MaxFilter(15))
        img_name =img_path+str(i)+".jpg"
        image.save(img_name)
        img_name_list.append(img_name)
        i+=1
    return img_name_list

# lptah =pdf_to_image('Invoices\Hoiio.pdf')
# print(lptah)