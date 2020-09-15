import json, os
import pandas as pd
with open("supplyinvoice\supply_csv.json") as sc:
    excel_date = json.load(sc)

class ExcelGeneration:
    def __init__(self):
        # with open("supply_csv.json") as sc:
        # self.excel_dict = excel_date
        self.excel_data_list =[]
        self.date_format = None
            
    def excel_creation(self,excel_list):
        for mapping_list in  excel_list:
            excel_dict = {}
            excel_dict = excel_date.copy() 
            for mapping_data in mapping_list:
                coloumn_value = mapping_data.get('extracted_value')
                if coloumn_value:
                    if mapping_data.get("csv_column"):
                        for sColumn in mapping_data['csv_column']:
                            excel_dict[sColumn] = coloumn_value
                if mapping_data.get("date_format"):
                    self.date_format =mapping_data['date_format']
            self.excel_dict_process(excel_dict)
            self.excel_data_list.append(excel_dict)
        excel_name = self.create_excel()
        return excel_name
    
    def create_excel(self):
        import datetime
        date_now = datetime.datetime.now()
        excel_name = "puchases_excel"+ date_now.strftime("%m%d%Y_%H%M%S")+".xlsx"
        df = pd.DataFrame(self.excel_data_list)
        print(df)
        excel_name = os.path.join(excel_name)
        print(excel_name)
        with pd.ExcelWriter(excel_name) as writer:
            df.to_excel(writer, sheet_name='Sheet_name_1') 
            return excel_name
            
    def excel_dict_process(self,excel_dict):
        excel_dict["Journal Memo"] = "PURCHASE; "+ excel_dict.get("Co./Last Name")
        if excel_dict.get("Date"):
            date_string = self.date_formating(excel_dict.get("Date"),date_return_format="%d-%m-%Y")
            excel_dict['Date'] = date_string
            
        if excel_dict.get("Currency Code"):
            if excel_dict.get("Currency Code") != "SGD":
                date = self.date_formating( excel_dict.get("Date"), date_format = "%d-%m-%Y")
                print(date)
                exchange_rate = self.get_exchange_rate(date,excel_dict.get("Currency Code"))
                excel_dict['Exchange Rate'] = exchange_rate
            else:
               excel_dict['Exchange Rate'] = 1
        excel_dict["Amount"] = self.remove_charactors(excel_dict.get("Amount")) if excel_dict.get("Amount") else 0
        excel_dict["Inc-Tax Amount"] = self.remove_charactors(excel_dict.get("Inc-Tax Amount")) if excel_dict.get("Inc-Tax Amount") else 0
        excel_dict["GST Amount"] = self.remove_charactors(excel_dict.get("GST Amount")) if excel_dict.get("GST Amount") else 0
        excel_dict["Amount Paid"] = self.remove_charactors(excel_dict.get("Amount Paid")) if excel_dict.get("Amount Paid") else 0
        
        
                
    def date_formating(self,date_string,date_return_format=None,date_format = None):
        if not date_format :
            date_format = self.date_format
        print("date_string",date_string)
        from datetime import datetime
        try:
            date_object = datetime.strptime(date_string,)
        except:
            import dateparser
            date_object = dateparser.parse(date_string)
        if date_return_format:
            new_date_string = date_object.strftime(date_return_format)
            print("new_date_string",new_date_string)
            return new_date_string
        else:
            return date_object
    

    def get_exchange_rate(self,date,currency):
        from forex_python.converter import CurrencyRates
        from currency_converter import CurrencyConverter
        from time import sleep
        currency = currency.strip()       
        try:
            currency_object = CurrencyRates()
            rate = currency_object.convert(str(currency),"SGD",1,date)
            sleep(10)
        except:
            currency_object = CurrencyConverter()
            rate = currency_object.convert(1,str(currency),"SGD",date)
        return rate
        
    def remove_charactors(self,text):
        import re
        text =  re.sub("[^0123456789\.,]","",text)
        return text