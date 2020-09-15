class ProcessingData:
    
    def __init__(self,img_data_list,mapping_list):
        self.img_data_list =img_data_list
        self.mapping_list = mapping_list
        
    def process_data(self):
        for map_data in self.mapping_list:
            # map_data = mapping_data.get("mapping")
            if map_data.get("type") =="label":
                # print("map_data",map_data)
                label_list = map_data.get("text").split()
                # print("label_list",label_list)
                map_data = self.find_label_in_img(label_list,map_data)
                map_data = self.find_coordinates(map_data)
            elif map_data.get('type') == 'value':
                map_data = self.set_value(map_data)
        from supplyinvoice.tesseract_operations import TesseractFunctions
        tf = TesseractFunctions()
        tf.process_with_mapping(self.mapping_list)
        return self.mapping_list
    
    def find_label_in_img(self,label_list,map_data):
        # print("label_list:",label_list)
        # print("map_data",map_data)
        for count in range(len(self.img_data_list)):
            # print("count",count)
            label_find =False
            img_data = self.img_data_list[count]
            if img_data.get("text") == label_list[0]:
                x,y,file_name = img_data.get("x"),img_data.get("y"),img_data.get("file")
                label_find =True
                # print(count,img_data)
                i=0
                for i in range(1,len(label_list)):
                    if label_list[i]:
                        # print(count+i,self.img_data_list[count+i])
                        next_img_data = self.img_data_list[count+i]
                        if next_img_data.get("text") != label_list[i]:
                            fuzzy_ratio = self.fuzzy_match(next_img_data.get("text"),label_list[i])
                            print(fuzzy_ratio)
                            if fuzzy_ratio<75:
                                label_find =False
                                break
                        else:
                            continue
                if  label_find == True:
                    map_data['x'] = x
                    map_data['y'] = y 
                    map_data['file_name']= file_name
                    return map_data
                else:
                    continue   
        return map_data 
    
    def find_coordinates(self,map_data):      
        if not map_data.get('x'):
           map_data['x'] = map_data.get('x_axics') 
        if not map_data.get('y'):
            map_data['y'] = map_data.get('y_axics')
        if not map_data.get('file_name'):
            map_data['file_name']= self.img_data_list[0]["file"]
        return map_data
    
    def set_value(self,map_data):
        if map_data.get('text'):
            map_data['extracted_value'] = map_data['text']
        return map_data    
    
    def fuzzy_match(self,text1,text2):
        from fuzzywuzzy import fuzz
        return fuzz.ratio(text1,text2)