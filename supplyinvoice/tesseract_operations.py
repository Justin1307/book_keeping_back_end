import pytesseract, os
import cv2
from PIL import Image
from pytesseract import Output

# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' #r'<full_path_to_your_tesseract_executable>'

class TesseractFunctions:
    def __init__(self):
        pass
    
    def image_to_string_conversion(self,img):
        img_text = pytesseract.image_to_string(img)
        return img_text
    
    def image_to_data_conversion(self,img,img_path):
        img_dict =pytesseract.image_to_data(img, output_type=Output.DICT)
        n_boxes = len(img_dict['level'])
        img_dict_list = []
        for i in range(n_boxes):
            if img_dict["conf"][i] !=  "-1":
            
                (x, y, w, h) = (img_dict['left'][i], img_dict['top'][i], img_dict['width'][i], img_dict['height'][i]) 
                img_dict_list.append({"x":x,"y":y,"w":w,"h":h,"text":img_dict["text"][i],"file":img_path})
        return (img_dict_list)
        
    def image_process(self,img_path,to_data=False):
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        if to_data:
            img_dict =self.image_to_data_conversion(img,img_path)
            return img_dict
        img_text = self.image_to_string_conversion(img)
        return img_text
    
    def process_with_mapping(self, mapping_list):
        for mapping_data in mapping_list:
            print(mapping_data)
            if mapping_data.get("type") == "label":
                img = cv2.imread(mapping_data.get("file_name"))
                img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
                w =mapping_data.get("width") if mapping_data.get("width") else mapping_data.get("w")
                h =mapping_data.get("height") if mapping_data.get("height") else mapping_data.get("h")
                x,y=mapping_data.get("x"),mapping_data.get("y")
                crop_img = img[y-15:y+h,x-10:x+w]
                text =self.image_to_string_conversion(crop_img)
                print(text)

                mapping_data['extracted_value'] =text
                cv2.imshow("Result", crop_img)
                # cv2.waitKey(0)
                self.remove_labels(mapping_data)
        
    def remove_labels(self, mapping_data):
        if mapping_data.get('text') in mapping_data.get('extracted_value'):
            print("extracted_value",mapping_data.get('extracted_value'))
            text =mapping_data.get('extracted_value').replace(mapping_data['text'],'')
            if ":" in text:
                text_split = text.split(":")
                text = text_split[1]
            text = text.strip('\n\x0c')
            print(text)
            mapping_data['extracted_value'] = text
        return mapping_data