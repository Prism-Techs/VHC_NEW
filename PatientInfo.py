from ast import Load
from datetime import datetime
from tkinter import messagebox
from dac_lib_soft import mup4728
import os.path
print_en = 0
import json

class PatientInfo :
     def __init__(self) :
         self.Name = ""
         self.Age = 0
         self.date = datetime.now()
         self.Gender = ""
         self.SLNo = -10
         self.eye  = ""
         self.CFF_F = 0.00
         self.CFF_P = 0.00
         self.f_mpod = 0.00
         self.f_sd = 0.00
         self.valueArray = [0]*2
         self.valueArray[0] = "0x20"
         self.valueArray[1] = "0x30"
         self.Alchohol = ""
         self.Smoking = ""
         self.Diabetes = ""
         self.Hypertension = ""
         raw_dt = datetime.now()
         self.log_date_time=raw_dt.strftime("%d/%m/%Y %I:%M:%S %p")

     def update_json(self):
        json_file_path = "patient_data/patient_latest.json"
        
        # Read existing JSON data
        try:
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            data = {}
        
        # Update the data with new information
        data.update({
            "CFF_F": self.CFF_F,
            "CFF_P": self.CFF_P,
            "f_mpod": self.f_mpod,
            "f_sd": self.f_sd,
        })
        
        # Write updated data back to JSON file
        with open(json_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        
        self.log_update("JSON file updated")


     def SetName(self,Name):
          self.Name= Name

     def SetDate(self, date):
         self.date = date

     def SetAge(self,age):
         self.Age = age
     
     def SetSlNo(self, slNo):
         self.SLNo = slNo         
         
     def setAlchohol_state(self,Alchohol):
         self.Alchohol = Alchohol        
        
     def setSmoking_state(self,Smoking):
         self.Smoking = Smoking
         
     def setDiabetes_state (self,Diabetes):
         self.Diabetes=Diabetes
         
     def setHypertension_state (self,Hypertension):
         self.Hypertension=Hypertension
         
     def SetEye(self, eye) :
         self.eye = eye

     def SetCFF_F(self, cff_f) :
         self.CFF_F = cff_f

     def SetCFF_P(self, cff_p):
         self.CFF_P = cff_p

     def SetF_mpod(self, mpod) :
         self.f_mpod = mpod        
     
     def SetF_SD(self, f_sd) :
         self.f_sd = f_sd

     def AddVales(self, val1, val2) :
        self.valueArray.__iadd__(val1)
        self.valueArray.__iadd__(val2)


     def getName(self):
          return self.Name

     def getAge(self):
         return self.Age 
     
     def getSlNo(self):
         return self.SLNo

     def getEye(self) :
         return self.eye 

     def getCFF_F(self) :
         return self.CFF_F 

     def getCFF_P(self):
         return self.CFF_P 

     def getetF_mpod(self) :
         return self.f_mpod 
        
     def getF_SD(self) :
         return self.f_sd 

     def getDate(self, date):
         return self.date 
     
     def Show(self):
         if print_en:
             print('Name :=' + self.Name)
             print('Gender : = ' + self.Gender)
                
     def UpdateResults(self) :
        if print_en:
             print('to be implemenetd')

#      def LoadSampleData(self):         
#              self.Name = "P1"
#              self.Age = 25
#              self.Gender = "M"
#              self.SLNo = 12120
#              self.eye  = "R"
#              self.CFF_F = 23
#              self.CFF_P = 45
#              self.f_mpod = 12
#              self.f_sd = 277
                  
             
            
     def log_update(self,log_data_update):
         raw_dt = datetime.now()
         time_now=raw_dt.strftime("%d/%m/%Y %I:%M:%S %p")
         fileName = "/home/pi/log_Data.txt"
         f = open(fileName, "a")
         f.write(time_now + "->"+log_data_update)
         f.write("\n")
         f.close()
         
     def log_update_pashent(self):
         raw_dt = datetime.now()
         time_now=raw_dt.strftime("%d/%m/%Y %I:%M:%S %p")
         fileName = "/home/pi/log_Data.txt"
         f = open(fileName, "a")
         f.write(time_now + "->"+str(self.SLNo)+",")
         f.write(str(self.Name) + ","+ str(self.Age)+","+self.Gender+","+self.eye + ",")
         f.write(self.Alchohol+","+self.Smoking+","+self.Diabetes+","+self.Hypertension)
         f.write("\n")
         f.close()
         
     
     #save data on to the disk.
     def Save_brk(self,file_locate):
         self.Show()
         self.log_update("save_brk_start")
         raw_dt = datetime.now()
         self.date=raw_dt.strftime("%d/%m/%Y %I:%M:%S %p")
         fileName = file_locate+"/"+self.Name + ".txt"
         f = open(fileName, "a")
         f.writelines(str(self.SLNo))
         f.write("\n")
         f.write("Name :" + self.Name)
         f.write("\n")
         f.write("tds :"+ str(self.date))
         f.write("\n")
         f.write("age :"+ str(self.Age))
         f.write("\n")
         f.write("gender :" +self.Gender)
         f.write("\n")
         f.write("eye :" + self.eye)         
         f.write("\n")
         f.write("Alchoholic :" + self.Alchohol)
         f.write("\n")
         f.write("Smoking" + self.Smoking)
         f.write("\n")
         f.write("Diabetes" + self.Diabetes)
         f.write("\n")
         f.write("Hypertension" +self.Hypertension)         
         f.write("\n")
         f.write("CFF_F:" + str(self.CFF_F))     
         f.write("\n")
         f.write("f-mpod:" + str(self.f_mpod))     
         f.write("\n")
         f.write("^^" + str(self.valueArray[0]))
         f.write("\n")
         f.write("^^" + str(self.valueArray[1]))
         f.write("\n")
         f.write("\n")
         f.close()
         if print_en:
             print("Save_brk done")
         self.log_update("Save_brk_done")
         self.update_json()

     def Save_brk_0(self,file_locate):
         self.Show()
         self.log_update("Save_brk_0_start")
         raw_dt = datetime.now()
         self.date=raw_dt.strftime("%d/%m/%Y %I:%M:%S %p")
         fileName = file_locate+"/"+self.Name + ".txt"
         f = open(fileName, "a")
         f.write("\n")
         f.writelines(str(self.SLNo))
         f.write("\n")
         f.write("Name :" + self.Name)
         f.write("\n")
         f.write("tds :"+ str(self.date))
         f.write("\n")
         f.write("age :"+ str(self.Age))
         f.write("\n")
         f.write("gender :" +self.Gender)
         f.write("\n")
         f.write("eye :" + self.eye)
         f.write("\n")
         f.write("Alchoholic :" + self.Alchohol)
         f.write("\n")
         f.write("Smoking :" + self.Smoking)
         f.write("\n")
         f.write("Diabetes :" + self.Diabetes)
         f.write("\n")
         f.write("Hypertension :" +self.Hypertension)
         f.write("\n")
         f.write("CFF_F:" + str(self.CFF_F))     
         f.write("\n")
         f.write("f-mpod:" +"0.00")     
         f.write("\n")
         f.write("^^" + str(self.valueArray[0]))
         f.write("\n")
         f.write("^^" + str(self.valueArray[1]))
         f.write("\n")
         f.write("\n")         
         f.close()
         if print_en:
             print("Save_brk_0 done")
         self.log_update("Save_brk_0_Done")
         self.update_json()


     def Save_brk_19(self,file_locate):
         self.Show()
         self.log_update("Save_brk_19_start")
         raw_dt = datetime.now()
         self.date=raw_dt.strftime("%d/%m/%Y %I:%M:%S %p")
         fileName = file_locate+"/"+self.Name + ".txt"
         f = open(fileName, "a")
         f.write("\n")
         f.writelines(str(self.SLNo))
         f.write("\n")
         f.write("Name :" + self.Name)
         f.write("\n")
         f.write("tds :"+ str(self.date))
         f.write("\n")
         f.write("age :"+ str(self.Age))
         f.write("\n")
         f.write("gender :" +self.Gender)
         f.write("\n")
         f.write("eye :" + self.eye)
         f.write("\n")
         f.write("Alchoholic :" + self.Alchohol)
         f.write("\n")
         f.write("Smoking; :" + self.Smoking)
         f.write("\n")
         f.write("Diabetes :" + self.Diabetes)
         f.write("\n")
         f.write("Hypertension :" +self.Hypertension)
         f.write("\n")
         f.write("CFF_F:" + str(self.CFF_F))     
         f.write("\n")
         f.write("f-mpod:" + "1.00+")     
         f.write("\n")
         f.write("^^" + str(self.valueArray[0]))
         f.write("\n")
         f.write("^^" + str(self.valueArray[1]))
         f.write("\n")
         f.write("\n")
         f.close()
         if print_en:
             print("Save_brk_19 done")
         self.log_update("Save_brk_19_done")
         self.update_json()


     def Save_brk_p(self,file_locate):
         self.Show()
         self.log_update("Save_brk_p_start")
         raw_dt = datetime.now()
         self.date=raw_dt.strftime("%d/%m/%Y %I:%M:%S %p")
         fileName = file_locate+"/"+self.Name + ".txt"
         f = open(fileName, "a")
         f.write("\n")
         f.writelines(str(self.SLNo))
         f.write("\n")
         f.write("Name :" + self.Name)
         f.write("\n")
         f.write("tds :"+ str(self.date))
         f.write("\n")
         f.write("age :"+ str(self.Age))
         f.write("\n")
         f.write("gender :" +self.Gender)
         f.write("\n")
         f.write("eye :" + self.eye)
         f.write("\n")
         f.write("Alchoholic :" + self.Alchohol)
         f.write("\n")
         f.write("Smoking :" + self.Smoking)
         f.write("\n")
         f.write("Diabetes :" + self.Diabetes)
         f.write("\n")
         f.write("Hypertension :" +self.Hypertension)
         f.write("\n")
         f.write("CFF_F:" + str(self.CFF_F))
         f.write("\n")
         f.write("CFF_P:" + str(self.CFF_P))
         f.write("\n")
         f.write("f-mpod:" + str(self.f_mpod))
         f.write("\n")
         f.write("f-sd:" + str(self.f_sd))
         f.write("\n")
         f.write("^^" + str(self.valueArray[0]))       
         f.write("\n")
         f.write("^^" + str(self.valueArray[1]))
         f.write("\n")
         f.write("\n")
         f.close()
         if print_en:
             print("Save_brk_p done")
         self.log_update("Save_brk_p_Done")
         self.update_json()



# def main(): 
#     pinfo = PatientInfo()
#     #pinfo.LoadSampleData()
#     pinfo.LoadSampleData()
# 
# 
# main()