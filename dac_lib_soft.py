import RPi.GPIO as GPIO
from smbus2 import SMBus
# from CFF_PARA_FOVEA import CffParaFovea as CffParaFovea
# from BRK_FOVEA_1 import BrkFovea_1 as BrkFovea_1
# from BRK_FOVEA_2 import BrkparaFovea as BrkparaFovea
import time

import math
# GPIO Pin Details
print_en = 0
DAC_lat = 4
B_F_I = 27
B_E = 12
G_F_I = 13
G_E = 26
SW_I = 20
switch = 20
BZ_I = 19
FN_E = 21
Disp = 22
flik_pin = 18
# Fixed Data
# DAC ADD-194
b_volt_val = [159,170,183,199,219,243,274,312,358,417,493,591,720,889,1111,1413,1817,2376,3161,3918] # 0 to 19 
# g_freq_val = int(80*x+2000) # 0 to 15
# red_led_val = int(4.80519*x-0.4329) # 0 da 20
# inner_ring_val = int(13.1948*x-0.329004) # 0 to 20
# DAC ADD-192
# Actuator_val = [0,142,1100,3680]  #0,1,2,3
Actuator_val = [0,142,1100,3680]  #0,1,2,3

# g_volt_val = int(85.4*x+0.380952,) # 0 to 20
# outer_ring_val= int(59.4*x-0.38095) # 0 to 20
#b_freq_val & b_frq_f_val 0 to 250
b_freq_val = [0,0,11,12,12,12,12,13,13,13,14,14,14,15,15,15,16,16,17,17,17,18,18,19,19,20,20,21,21,21,22,23,23,24,24,25,25,26,27,27,28,28,29,30,31,31,32,33,34,34,35,36,37,38,39,40,40,41,42,43,44,45,47,48,49,50,51,52,54,55,56,57,59,60,62,63,64,66,67,69,71,72,74,76,78,79,81,83,85,87,89,91,93,96,98,100,102,105,107,110,112,115,118,120,123,126,129,132,135,138,142,145,148,152,155,159,163,166,170,174,178,183,187,191,196,200,205,210,215,220,225,230,235,241,246,252,258,264,270,277,283,290,296,303,310,318,325,333,340,348,356,365,373,382,391,400,409,419,429,439,449,459,470,481,492,504,516,528,540,552,565,579,592,606,620,634,649,664,680,696,712,729,746,763,781,799,818,837,856,876,896,917,939,961,983,1006,1029,1053,1078,1103,1129,1155,1182,1210,1238,1267,1296,1326,1357,1389,1421,1454,1488,1523,1558,1595,1632,1670,1709,1749,1790,1831,1874,1918,1962,2008,2055,2103,2152,2202,2253,2306,2359,2414,2471,2528,2587,2647,2709,2772,2837,2903,2971,3040,3111,3183,3257,3333,3411,3490,3572]

#Blue null addon for 0 to 19
# b_null_set_addon = round( 0.123457*x-0.148366 ,2) # (1  to 18) lv 0,19 
#b_freq_val & b_frq_f_val 0 to 250
# Frq value
b_frq_f_val = [8.06,8.218,12.74,13.45,13.45,13.45,13.45,14.21,14.21,14.21,14.93,14.93,14.93,15.64,15.64,15.64,16.4,16.4,17.15,17.15,17.15,17.89,17.89,18.62,18.62,19.63,19.36,20.1,20.1,20.1,20.83,21.59,21.59,22.36,22.36,23.09,23.09,23.82,24.56,24.58,25.28,25.28,26.02,26.77,27.51,27.51,28.28,28.99,29.75,29.75,30.5,31.24,31.97,33.71,33.45,34.18,34.18,34.95,35.67,36.42,37.16,37.93,39.42,40.18,40.88,41.6,42.38,43.13,44.52,45.31,46.04,46.78,48.27,49.7,50.5,51.16,52.09,53.66,54.49,56.16,57.78,58.62,60.32,61.86,63.42,64.32,65.98,67.6,69.26,70.82,72.49,74.06,75.86,78.19,79.92,81.56,83.05,85.72,87.26,89.76,91.49,93.84,96.3,97.94,100.4,102.8,105.4,107.7,110.1,112.5,115.6,118.1,120.5,123.6,126,129.1,132.4,134.7,137.8,141,144.2,148,151.3,154.5,158.7,162,166.1,170.2,174.4,178.5,182.7,186.8,190.9,196,200.1,205.1,210,214.8,219.5,225.1,229.8,235.4,240.2,245.7,251.3,257.6,263.5,270,275.8,282.5,289.1,296.6,303.2,310.7,318,325.2,332.3,340.2,348.2,356.2,364.2,372.8,382.2,391.7,401.2,411.6,421.7,431.3,441.1,450.5,460.9,472.3,483.1,494.9,506.6,518.4,530.8,542.7,555.6,568.5,581.6,595.4,609.4,623.2,637.7,652,667.2,682.6,698,714.3,730.6,747.2,764.6,782,800.8,820.5,840,859.2,879.3,899.8,921.4,942.8,964.2,986.3,1009,1033,1057,1081,1106,1133,1159,1185,1213,1242,1271,1300,1331,1363,1394,1427,1461,1494,1529,1566,1601,1639,1678,1716,1756,1797,1838,1884,1924,1968,2014,2061,2110,2157,2208,2259,2312,2365,2420,2477,2535,2594,2653,2717,2781,2847,2915] 
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 

flicker_delay =  0.043
cff_delay = 0.209
brk_delay = 0.125

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# # dac.MOTOR(1260)
# # dac.GREEN_Volt(950)
# # dac.GREEN_FREQ(1350)
motor_possition_1 = 75     #DAC VAL
motor_possition_2 = 1250    #DAC VAL
red_led_on =  65              #DAC VAL
red_led_off = 0               #DAC VAL
inner_led_on = 730
inner_led_off = 0
outer_led_on = 155
outer_led_off = 0

green_led_freq_on = 2000
green_led_freq_off = 0
green_led_volt_on = 1000
green_led_volt_off = 0
buzz_freq = 9000
buzz_tim_on = .01
buzz_tim_off = .210
buzz_duty = 50

blue_led_bkf_freq = 274
blue_led_freq_off = 0

blue_led_bkf_volt = 360
blue_led_volt_off = 0
# blue_volt_nul = 1

blue_led_Volt_offset =2
blue_led_Freq_offset =5

# dac.D1("ON")
# dac = mup4728(0x61)
# dac.MOTOR(400)#A4 MOTOR
# dac.BLUE_FREQ(0)#A0 BLUE_FREQ 
# dac.BLUE_Volt(4095)#A5 BLUE_volt 
# dac.GREEN_FREQ(1221)#A1 GREEN_FREQ 
# dac.GREEN_Volt(1065)#A6 GREEN_volt
# dac.INNER_LED(175)#A2 INNER LED
# dac.RED_LED(0)#A7  RED LED
# dac.OUTER_LED(500)#A3 OUTER RING

class mup4728: 
        DAC = SMBus(1)       
        def __init__(self,dac_addr):            
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)            
            GPIO.setup(B_F_I,GPIO.IN)#D0 Blue Freq in
            GPIO.setup(B_E,GPIO.OUT)#D1 Blue Enable 
            GPIO.setup(G_F_I,GPIO.IN)#D2 Green Freq in
            GPIO.setup(G_E,GPIO.OUT)#D3 Green Enable
            GPIO.setup(BZ_I,GPIO.OUT)#D4 Buzz 
            GPIO.setup(SW_I,GPIO.IN)#D5 Switch
            GPIO.setup(FN_E,GPIO.OUT)#D6 Fan
            GPIO.setup(Disp,GPIO.OUT)#D7 Disp Enable
            GPIO.setup(flik_pin,GPIO.OUT)
            GPIO.setup(DAC_lat,GPIO.OUT)# DAC Latch
            self.last_inner_value = None  # Track last set value
            self.last_inner_time = 0  # Track last update time
            self.dac_lock = False  # Prevent concurrent DAC writes
            GPIO.output(DAC_lat,GPIO.HIGH) # DAC Latch
            GPIO.output(B_E,GPIO.LOW)#D1 Blue Enable
            GPIO.output(G_E,GPIO.LOW)#D3 Green Enable
            GPIO.output(FN_E,GPIO.HIGH)#D6 Fan
            self.dac_addr=dac_addr
            
            data = [ 0, 0]
            self.on_time = 0
            self.skip_main = 0
            self.back_flicker = 0
            self.freq = 35
            self.pwm_run = 0
            self.buzz_freq = buzz_freq
            self.dac_ch = [0,8,16,24,32,40,48,56]
            
            # self.cff_fovea_list=[0,0,0,0,0] #5 val
            self.cff_fovea_min =[0,0,0,0,0] #5 val
            self.cff_fovea_max = 0
            self.cff_fovea_avg = 0

            self.brk_f_null_1 = 0
            self.brk_fovea_min = [0,0,0,0,0]
            self.brk_fovea_mid = [0,0,0,0,0]
            self.brk_fovea_max = [0,0,0,0,0]

            # self.cff_para_f_list=[0,0,0,0,0] #5 val
            self.cff_para_f_min = [0,0,0,0,0] #5 val
            self.cff_para_f_max = 0
            self.cff_para_f_avg = 0

            self.brk_para_f_min=[0,0,0,0,0]
            self.brk_para_f_mid=[0,0,0,0,0]
            self.brk_para_f_max=[0,0,0,0,0]
#             for 
#             self.DAC.write_i2c_block_data(self.dac_addr, self.dac_ch[0], data)                        
            self.cff_fovea_frq = 35
            self.brk_fovea_frq = 160            
            self.cff_para_fovea_frq = 35 
            self.brk_para_fovea_frq = 0   
            self.blue_volt_nul = 1
            self.save_no = 0
            #self.b_volt_val= b_volt_val
            self.b_frq_val =160
            self.blue_led_freq_val= 0
            self.f_mpod =0.00
            self.f_sd =0.00
            GPIO.output(DAC_lat,GPIO.LOW)
            self.DAC.write_i2c_block_data(self.dac_addr, self.dac_ch[0], data)
            self.DAC.write_i2c_block_data(self.dac_addr, self.dac_ch[1], data)
            self.DAC.write_i2c_block_data(self.dac_addr, self.dac_ch[2], data)
            self.DAC.write_i2c_block_data(self.dac_addr, self.dac_ch[3], data)
            self.DAC.write_i2c_block_data(self.dac_addr, self.dac_ch[4], data)
            self.DAC.write_i2c_block_data(self.dac_addr, self.dac_ch[5], data)
            self.DAC.write_i2c_block_data(self.dac_addr, self.dac_ch[6], data)
            self.DAC.write_i2c_block_data(self.dac_addr, self.dac_ch[7], data)
            GPIO.output(DAC_lat,GPIO.HIGH)
            self.p=GPIO.PWM(flik_pin,self.freq)
            self.buz=GPIO.PWM(BZ_I,self.buzz_freq)
            
        def clr_pre_data (self):
            # self.cff_fovea_list=[0,0,0,0,0] #5 val
            self.cff_fovea_min =[0,0,0,0,0] #5 val
            self.cff_fovea_max = 0
            self.cff_fovea_avg = 0

            self.brk_f_null_1 = 0
            self.brk_fovea_min = [0,0,0,0,0]
            self.brk_fovea_mid = [0,0,0,0,0]
            self.brk_fovea_max = [0,0,0,0,0]

            # self.cff_para_f_list=[0,0,0,0,0] #5 val
            self.cff_para_f_min = [0,0,0,0,0] #5 val
            self.cff_para_f_max = 0
            self.cff_para_f_avg = 0

            self.brk_para_f_min=[0,0,0,0,0]
            self.brk_para_f_mid=[0,0,0,0,0]
            self.brk_para_f_max=[0,0,0,0,0]
#             for 
#             self.DAC.write_i2c_block_data(self.dac_addr, self.dac_ch[0], data)                        
            self.cff_fovea_frq = 35
            self.brk_fovea_frq = 160            
            self.cff_para_fovea_frq = 35 
            self.brk_para_fovea_frq = 0   
            self.blue_volt_nul = 1
            
        def get_print(self,data):
            if print_en == 1:
                print(data)
                
        def MOTOR(self,in_data):
            GPIO.output(DAC_lat,GPIO.LOW)
            str_data = 'MOTOR_data = '+str(in_data)
            self.get_print(str_data)
            in_data = in_data
            data = [int(in_data / 256)+128, int(in_data % 256)]
            self.DAC.write_i2c_block_data(self.dac_addr, self.dac_ch[0], data)            
            GPIO.output(DAC_lat,GPIO.HIGH)
            
        def BLUE_FREQ(self,in_data):
            GPIO.output(DAC_lat,GPIO.LOW)
            str_data = 'BLUE_FREQ_data = ' + str(in_data)
            self.get_print(str_data)
            in_data = in_data/1.32 
            data = [ int(in_data / 256), int(in_data % 256)]             
            self.DAC.write_i2c_block_data(self.dac_addr, self.dac_ch[1], data)
            GPIO.output(DAC_lat,GPIO.HIGH)
            
        def BLUE_Volt(self,in_data):
            GPIO.output(DAC_lat,GPIO.LOW)
            str_data = 'BLUE_Volt_data = ' + str(in_data)
            self.get_print(str_data)
            in_data = in_data   
            data = [ int(in_data / 256), int(in_data % 256)]                        
            self.DAC.write_i2c_block_data(self.dac_addr, self.dac_ch[2], data)            
            GPIO.output(DAC_lat,GPIO.HIGH)
            
        def GREEN_FREQ(self,in_data):
            GPIO.output(DAC_lat,GPIO.LOW)
            str_data = 'GREEN_FREQ_data = ' + str(in_data)
            self.get_print(str_data) 
            in_data = in_data/1.62
            data = [ int(in_data / 256), int(in_data % 256)]                      
            self.DAC.write_i2c_block_data(self.dac_addr, self.dac_ch[3], data)
            GPIO.output(DAC_lat,GPIO.HIGH)
            
        def GREEN_Volt(self,in_data):
            GPIO.output(DAC_lat,GPIO.LOW)
            str_data = 'GREEN_Volt_data = ' + str(in_data)
            self.get_print(str_data) 
            in_data = in_data/1.6
            print(in_data)      
            data = [ int(in_data / 256), int(in_data % 256)]   
            print(data)                    
            self.DAC.write_i2c_block_data(self.dac_addr, self.dac_ch[4], data)
            GPIO.output(DAC_lat,GPIO.HIGH)
            
        def INNER_LED(self,in_data):
            GPIO.output(DAC_lat,GPIO.LOW)
            str_data = 'INNER_LED_data = ' + str(in_data)
            self.get_print(str_data)    
            in_data = in_data   
            data = [ int(in_data / 256), int(in_data % 256)]
            # data = [ 1, 1]
            print(data)
            self.DAC.write_i2c_block_data(self.dac_addr, self.dac_ch[5], data)
            GPIO.output(DAC_lat,GPIO.HIGH)
            time.sleep(0.3)
            
        def RED_LED(self,in_data):
            GPIO.output(DAC_lat,GPIO.LOW)
            str_data = 'RED_LED_data = ' + str(in_data)
            self.get_print(str_data)   
            in_data = in_data/3            
            data = [ int(in_data / 256)+128, int(in_data % 256)]
            self.DAC.write_i2c_block_data(self.dac_addr, self.dac_ch[6], data)
            GPIO.output(DAC_lat,GPIO.HIGH)
            
        def OUTER_LED(self,in_data):
            GPIO.output(DAC_lat,GPIO.LOW)
            str_data = 'OUTER_LED_data = ' + str(in_data)
            self.get_print(str_data)
            in_data = in_data/1.68
            data = [ int(in_data / 256), int(in_data % 256)]
            self.DAC.write_i2c_block_data(self.dac_addr, self.dac_ch[7], data)
            GPIO.output(DAC_lat,GPIO.HIGH)
                        
        def buzzer_on(self):
            self.get_print('buzzer_on')
            self.buz.start(buzz_duty)
            self.buz.ChangeFrequency(self.buzz_freq)
#             GPIO.output(BZ_I,GPIO.HIGH)#D4 Buzz
            
        def buzzer_off(self):
            self.get_print('buzzer_off')
            self.buz.stop()
#             GPIO.output(BZ_I,GPIO.LOW)#D4 Buzz
            
        def buzzer_1(self):
            self.get_print('buzzer_1')
            self.buzzer_on()#D4 Buzz
            time.sleep(buzz_tim_on)
            self.buzzer_off()#D4 Buzz
#             time.sleep(buzz_tim_off)
            
        def buzzer_3(self):
            self.get_print('buzzer_3')
            for x in range(3):
                self.buzzer_on()#D4 Buzz
                time.sleep(buzz_tim_on)
                self.buzzer_off()#D4 Buzz
                time.sleep(buzz_tim_off)
                
        def fan_on(self):
            self.get_print('fan_on')
            GPIO.output(FN_E,GPIO.HIGH)#D6 Fan
        
        def fan_off(self):
            self.get_print('fan_off')
            GPIO.output(FN_E,GPIO.LOW)#D6 Fan
        
        def display_on(self):
            self.get_print('display_on')
            GPIO.output(Disp,GPIO.HIGH)#D7 Disp Enable
        
        def display_off(self):
            self.get_print('display_off')
            GPIO.output(Disp,GPIO.LOW)#D7 Disp Enable
        
#################################################################################################
        def actuator_control(self,in_data): 
            self.MOTOR(Actuator_val[in_data])
#-----------------------------------------------------------------------------------
        def green_volt_control(self,data_in):
            if(0<=data_in<=20):
                dac_val=int(600*data_in+0.380952) # 0 to 20
                str_data = 'GREEN_Volt_DAC = ' + str(dac_val)
                self.get_print(str_data)
                self.GREEN_Volt(dac_val)              
            else :
                str_data = 'GREEN_Volt_DAC must be 0 to 20 ' + str(dac_val)
                self.get_print(str_data)

        def green_freq_control(self,data_in):
            if(0<=data_in<=15):
                dac_val=int(80*data_in+4000) # 0 to 15
                str_data = 'GREEN_FREQ_DAC = ' + str(dac_val)
                self.get_print(str_data)
                self.GREEN_FREQ(dac_val) 
            elif(data_in == 16):
                dac_val= 0 # 16th
                str_data = 'GREEN_FREQ_DAC = ' + str(dac_val)
                self.get_print(str_data)
                self.GREEN_FREQ(dac_val)                
            else :
                str_data = 'GREEN_FREQ_DAC must be 0 to 20 ' + str(dac_val)
                self.get_print(str_data)           
#-----------------------------------------------------------------------------------
        def blue_led_volt_control(self,mode,val):
            if mode == 0:
                if (0 <= val <= 19):
                    b_volt=int(b_volt_val[val]*1.95)
                    self.blue_volt_nul = val
                    str_data = 'blue_led_Volt(nul='+str(val)+') =' + str(b_volt)
                    self.get_print(str_data) 
                    self.BLUE_Volt(b_volt)#A5 BLUE_volt                    
                else: 
                    self.get_print('Blue Volt Beyond range')
            if mode == 1:
                if (1 <= val <= 20):
                    b_volt=int((7.79398*val-4.93684)/1.25)                  
                    str_data = 'blue_led_Volt(eq1) =' + str(b_volt)
                    self.get_print(str_data) 
                    self.BLUE_Volt(b_volt)#A5 BLUE_volt
                else: 
                    self.get_print('Blue Volt Beyond range')
            if mode == 2:
                if (1 <= val <= 20):
                    b_volt=int((24.606*val-23.4632)/1.25)
                    str_data = 'blue_led_Volt(eq2) =' + str(b_volt)
                    self.get_print(str_data) 
                    self.BLUE_Volt(b_volt)#A5 BLUE_volt
                else: 
                    self.get_print('Blue Volt Beyond range')
            if mode == 3:
                if (0 <= val <= 20):
                    b_volt=int((28.8*val+0.4)/1)
                    str_data = 'blue_led_Volt(eq3) =' + str(b_volt)
                    self.get_print(str_data) 
                    self.BLUE_Volt(b_volt)#A5 BLUE_volt
                else: 
                    self.get_print('Blue Volt Beyond range')
                
        def blue_led_Freq_control(self,val):
            if (0 <= val <= 250):
                b_frq =int(b_frq_f_val[val])
                str_data = 'blue_led_Freq =' + str(val)
                self.get_print(str_data) 
                self.BLUE_FREQ(b_frq)#A5 BLUE_volt  
                self.brk_fovea_frq=val              
            else:                
                self.get_print('Blue Volt Beyond range')
#-----------------------------------------------------------------------------------
        def inner_led_control(self,data_in):
            print("called")
            if data_in == 0:
                dac_val = 0
                self.INNER_LED(dac_val)
            if(0<=data_in<=20):
                dac_val = 257
                str_data = 'INNER_LED_DAC = ' + str(dac_val)
                self.get_print(str_data)
                self.INNER_LED(dac_val)
            else :
                str_data = 'INNER_LED_DAC must be 0 to 20 ' + str(dac_val)
                self.get_print(str_data)

        def reset_inner_led(self):
                """Reset Inner LED to a known state."""
                self.get_print("Resetting Inner LED")
                self.INNER_LED(0)  # Turn off completely
                time.sleep(0.1)    # Wait for stability
                self.last_inner_value = None  # Clear last value


        def outer_led_control(self,data_in):
            if(0<=data_in<=20):
                dac_val=int(110.4*data_in-0.38095) # 0 to 20
                str_data = 'OUTER_LED_DAC = ' + str(dac_val)
                self.get_print(str_data)
                self.OUTER_LED(dac_val)
            else :
                str_data = 'OUTER_LED_DAC must be 0 to 20 ' + str(dac_val)
                self.get_print(str_data)

        def red_led_control(self,data_in):
            if(0<=data_in<=20):
                    #dac_val=int(4.80519*data_in-0.4329) # 0 to 20
                    dac_val = int(204.75 * data_in)  # For data_in=20, dac_val=4095
                    str_data = 'RED_LED_DAC = ' + str(dac_val)
                    self.get_print(str_data)
                    self.RED_LED(dac_val)
            else:
                str_data = 'RED_LED_DAC must be 0 to 20 ' + str(dac_val)
                self.get_print(str_data)

#################################################################################################

        def fliker_start_g(self):            
            GPIO.output(G_E,GPIO.HIGH)#D3 Green Enable
            GPIO.output(B_E,GPIO.LOW)#D3 Blue Enable
            if (not self.pwm_run):                
                self.p.start(80.4)
                self.pwm_run = 1
                self.get_print('fliker_start_g')                
                
        def fliker_start_b(self):            
            GPIO.output(G_E,GPIO.HIGH)#D3 Green Enable
            GPIO.output(B_E,GPIO.HIGH)#D3 Blue Enable
            if (not self.pwm_run):                
                self.p.start(50.0)
                self.pwm_run = 1   
                self.get_print('fliker_start_b')             
            
        def fliker_Freq(self,frq):
            self.freq = frq
            if (self.pwm_run):
                str_data = 'fliker_Freq = ' + str(self.freq)
                self.get_print(str_data)                  
                if self.freq > 0 :
                    self.p.ChangeFrequency(self.freq)
                
        def fliker_stop(self):            
            if (self.pwm_run):
                self.p.stop()
                self.pwm_run = 0
                str_data = 'fliker_stop = ' + str(self.pwm_run)
                self.get_print(str_data)                
                GPIO.output(G_E,GPIO.HIGH)#D3 Green Enable
                GPIO.output(B_E,GPIO.LOW)#D3 Blue Enable
                
        def green_led_on(self):
            if (self.pwm_run):
                self.p.stop()
                self.pwm_run = 0
                self.get_print('green_led_on')
                GPIO.output(flik_pin,GPIO.HIGH)#D7 Disp Enable
                GPIO.output(G_E,GPIO.HIGH)#D3 Green Enable
            else:
                self.get_print('green_led_on')
                GPIO.output(flik_pin,GPIO.HIGH)#D7 Disp Enable
                GPIO.output(G_E,GPIO.HIGH)#D3 Green Enable
            
        def green_led_off(self):
            self.get_print('green_led_off')
            GPIO.output(G_E,GPIO.LOW)#D3 Green Enable
            
        def blue_led_on(self):
            if (self.pwm_run):
                self.get_print('blue_led_on')
                self.p.stop()
                self.pwm_run = 0
                GPIO.output(flik_pin,GPIO.LOW)#D7 Disp Enable
                GPIO.output(B_E,GPIO.HIGH)#D3 Green Enable
            else:
                self.get_print('blue_led_on')
                GPIO.output(flik_pin,GPIO.LOW)#D7 Disp Enable
                GPIO.output(B_E,GPIO.HIGH)#D3 Green Enable        
        
        def blue_led_off(self): 
            self.get_print('blue_led_off')
            GPIO.output(B_E,GPIO.LOW)#D3 Green Enable       

        def get_blue_volt_nul(self): 
            return(self.blue_volt_nul)
        
        def put_blue_volt_nul(self,val):
            self.blue_volt_nul = val
        
        def get_blue_freq(self,data_in):
            return(b_frq_f_val[data_in])     

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
        def get_flicker_delay (self):
            return(flicker_delay)

        def get_cff_delay (self):
            return(cff_delay)

        def get_brk_delay (self):
            return(brk_delay)
        
        def fliker(self,val):
            self.green_freq_control(val)
            

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                
        
        def get_cff_f_min_cal (self,locate,in_val):
            if(locate == 0):
                self.cff_fovea_min[locate] = in_val
            else:
                self.cff_fovea_min[locate] = round(((sum(self.cff_fovea_min) + in_val)/(locate+1)),1)
            str_data = 'dac_cff_min = ' + str(self.cff_fovea_min[locate])+'locate='+str(locate)
            self.get_print(str_data)                 
            return(self.cff_fovea_min[locate])
       
        def get_cff_f_max_cal (self):
            data= self.cff_fovea_min
            val=sorted(data)
            self.cff_fovea_max = round(((sum(val)-val[0]-val[len(val)-1])/3),1)
            str_data = 'cff_f_max = ' + str(self.cff_fovea_max)
            self.get_print(str_data)            
            return(self.cff_fovea_max)

        def get_cff_f_avg_cal (self):
            self.cff_fovea_avg = ((self.cff_fovea_min[4] + self.cff_fovea_max)/2)-3.5
            self.cff_fovea_avg = round(self.cff_fovea_avg,1) 
            self.cff_fovea_frq = self.cff_fovea_avg
            str_data = 'cff_f_avg = ' + str(self.cff_fovea_avg)
            self.get_print(str_data)
            return(self.cff_fovea_avg)

        def get_cff_f_min_all (self):
            return(self.cff_fovea_min)

        def get_cff_f_max_all (self):
            return(self.cff_fovea_max)

        def get_cff_f_avg_all (self):
            return(self.cff_fovea_avg)        

        def get_cff_fovea_frq(self):
            return(self.cff_fovea_frq)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
        
        def get_cff_p_min_cal (self,locate,in_val):
            if(locate == 0):
                self.cff_para_f_min[locate] = in_val
            else:
                self.cff_para_f_min[locate] = round(((sum(self.cff_para_f_min) + in_val)/(locate+1)),1)
            str_data = 'dac_cff_min = ' + str(self.cff_para_f_min[locate])+'locate='+str(locate)
            self.get_print(str_data)                 
            return(self.cff_para_f_min[locate])

        def get_cff_p_max_cal (self):
            data = self.cff_para_f_min
            val=sorted(data)        
            self.cff_para_f_max = round(((sum(val)-val[0]-val[len(val)-1])/3),1)    
            str_data = 'cff_p_max = ' + str(self.cff_para_f_max)
            self.get_print(str_data)            
            return(self.cff_para_f_max)
        
        def put_cff_p_avg_cal (self,data_in):            
            self.cff_para_f_avg = round(data_in,1)
           
        def get_cff_p_avg_cal (self):
            self.cff_para_f_avg = round(((self.cff_para_f_min[4] + self.cff_para_f_max)/2),1)-3.5
            self.cff_para_fovea_frq = self.cff_para_f_avg
            return(self.cff_para_f_avg) 

        def get_cff_p_min_all (self):
            return(self.cff_para_f_min)

        def get_cff_p_max_all (self):
            return(self.cff_para_f_max)

        def get_cff_p_avg_all (self):
            return(self.cff_para_f_avg)

        def get_cff_para_fovea_frq(self):
            return(self.cff_para_fovea_frq)

        def put_cff_para_fovea_frq(self,cff_para_fovea_frq):
            self.cff_para_fovea_frq = round(cff_para_fovea_frq,1)
            self.fliker_Freq(self.cff_para_fovea_frq)        

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 

        def put_cff_fovea_frq(self,cff_fovea_frq):
            self.cff_fovea_frq = round(cff_fovea_frq,1)
            self.fliker_Freq(self.cff_fovea_frq)
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

##################################################################################################
#             self.brk_fovea_min = [0,0,0,0,0]
#             self.brk_fovea_mid = [0,0,0,0,0]
#             self.brk_fovea_max = [0,0,0,0,0]

        def get_brk_fovea_min_all(self):
            return(self.brk_fovea_min)

        def get_brk_fovea_mid_all(self):
            return(self.brk_fovea_mid)

        def get_brk_fovea_max_all(self):
            return(self.brk_fovea_max)

        def put_brk_fovea_min(self,in_data):
            self.brk_fovea_min=in_data

        def put_brk_fovea_mid(self,in_data):
            self.brk_fovea_mid=in_data

        def put_brk_fovea_max(self,in_data):
            self.brk_fovea_max=in_data

        def roundup (self,val):
            int_val = int(val)
            if (int_val < val):
                return (int_val+1)
            else:
                return (int_val)

        def get_brk_fovea_mid_calc(self,locate,brk_min,brk_max):
            self.brk_fovea_min[locate] = brk_min                
            self.brk_fovea_max[locate] = brk_max
            if locate == 0:                
                self.brk_fovea_mid[locate] = self.roundup((((brk_min+brk_max))/2)-1)
                return(self.brk_fovea_mid[locate])
            else:                
                self.brk_fovea_mid[locate] = self.roundup((sum(self.brk_fovea_min)+sum(self.brk_fovea_max)-(self.brk_fovea_min[0])-(self.brk_fovea_max[0]))/(2*locate)-1)
                return(self.brk_fovea_mid[locate])

        def get_brk_fovea_frq(self,brk_val):
            return(b_frq_f_val[brk_val])

        def back_flicker(self):
            back_flicker_en = 1

     
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
       
        def get_brk_para_f_min_all(self):
            return(self.brk_para_f_min)

        def get_brk_para_f_mid_all(self):
            return(self.brk_para_f_mid)

        def get_brk_para_f_max_all(self):
            return(self.brk_para_f_max)   

        def put_brk_para_f_min(self,in_data):
            self.brk_para_f_min=in_data

        def put_brk_para_f_mid(self,in_data):
            self.brk_para_f_mid=in_data

        def put_brk_para_f_max(self,in_data):
            self.brk_para_f_max=in_data

        def get_brk_para_f_mid_calc(self,locate,brk_min,brk_max):
            self.brk_para_f_min[locate] = brk_min                
            self.brk_para_f_max[locate] = brk_max
            if locate == 0:                
                self.brk_para_f_mid[locate] = self.roundup((((brk_min+brk_max))/2)-1)
                return(self.brk_para_f_mid[locate])
            else:                
                self.brk_para_f_mid[locate] = self.roundup((sum(self.brk_para_f_min)+sum(self.brk_para_f_max)-(self.brk_para_f_min[0])-(self.brk_para_f_max[0]))/(2*locate)-1)
                return(self.brk_para_f_mid[locate])

        def get_brk_para_f_frq(self,brk_val):
            return(b_frq_f_val[brk_val])

        # def put_brk_para_fovea_frq
##################################################################################################
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

        def get_cal_f_mpod(self):            
            a = b_frq_f_val[self.brk_fovea_mid[4]]
            b = b_frq_f_val[self.brk_para_f_mid[4]]
            print("brk_F = ",a ,"brk_PF = ",b)
            val_1 = round(0.3*math.log10(a/b),2)
            val_2 = round(abs(0.123457*(self.blue_volt_nul)-0.148366)-0.01,2)
            print("val_1=",val_1)
            print("val_2=",val_2)
            val = round(val_1 + val_2,2)
            str_data = 'mpod = ' + str(val)
            self.get_print(str_data)
            self.f_mpod = val
            return(val)
        
        def get_cal_f_sd(self):            
            brk_f_min =b_frq_f_val[ min(self.brk_fovea_mid)]
            brk_p_min =b_frq_f_val[ min(self.brk_para_f_mid)]
            brk_f_max =b_frq_f_val[ max(self.brk_fovea_mid)]
            brk_p_max =b_frq_f_val[ max(self.brk_para_f_mid)]
            val_min   = round(0.3*math.log10(brk_f_min/brk_p_min) + abs(0.123457*(self.blue_volt_nul)-0.148366) ,2)
            val_max   = round(0.3*math.log10(brk_f_max/brk_p_max) + abs(0.123457*(self.blue_volt_nul)-0.148366) ,2)
            print("val_min=",val_min)
            print("val_max=",val_max)
            val_cal   = round(abs(round(abs(val_max + val_min)/2,2)-self.f_mpod),2)
            str_data = 'SD = ' + str(val_cal)
            self.get_print(str_data) 
            return(val_cal)
        
#-------------------------------------------------------------------------------------------------------------------------
        # def map(x, in_min,in_max,out_min,out_max):
        #     return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$    
        def get_save_no(self):
            return(self.save_no)

        def put_save_no(self,save_no):
            self.save_no = save_no                
        

        # def patient_switch_enable_select(self,select) :
        #     if (select == 1):
        #         self.get_print('CffFovea.handleReStart interrupt')
        #         GPIO.add_event_detect(switch,GPIO.RISING,callback=CffFovea.handleuserButton)
        #     elif (select == 2):
        #         self.get_print('brk_fovea.handleReStart interrupt')
        #         GPIO.add_event_detect(switch,GPIO.RISING,callback=BrkFovea_1.handleuser) 
        #     elif select == 3 :
        #         self.get_print('Cff_para_Fovea.handleReStart interrupt')
        #         GPIO.add_event_detect(switch,GPIO.RISING,callback=CffParaFovea.userButten_handle)
        #     elif select == 4 :
        #         self.get_print('brk_para_fovea.handleReStart interrupt')
        #         GPIO.add_event_detect(switch,GPIO.RISING,callback=BrkparaFovea.handleuser)
        #     else :
        #         self.get_print('out of range')
                
#         def patient_switch_desable(self) :
#             self.get_print('GPIO relese interrupt')
#             GPIO.remove_event_detect(switch)

        def all_led_off (self):
            self.get_print('all_led_off-----------')      
            self.fan_on()
            self.display_on()
            self.blue_led_Freq_control(0) #0 to 250
            self.blue_led_volt_control(3,0) #0(0 to 19), 1(1 to 20), 2(1 to 20), 3(0 to 20)
            self.green_volt_control(0) #0 to 20
            self.green_freq_control(16) # Flicker null value (0 to 15) and 16 = 0
            self.inner_led_control(0) #0 to 20
            self.outer_led_control(0) #0 to 20
            self.red_led_control(0) #0 to 20
            self.fliker_stop()
            self.green_led_off()
            self.blue_led_off()
            self.get_print('all_led_off++++++++++++++++++')
        
        def skip_main_rset(self):
            self.skip_main = 0
            
        def skip_main_set(self):
            self.skip_main = 1
            
        def black_screen_initialize(self):
            self.all_led_off()
            
        def main_Prepair (self):  
            if (self.back_flicker == 0 and (not self.skip_main)) :
                self.skip_main_set()
                self.get_print('main_Prepair--------------------')            
                if (self.on_time == 0):
                    self.blue_led_volt_control(3,0) #0(0 to 19), 1(1 to 20), 2(1 to 20), 3(0 to 20)
                    self.green_freq_control(16) # Flicker null value (0 to 15) and 16 = 0
                    self.red_led_control(0) #0 to 20
                    self.inner_led_control(0) #0 to 20
                    self.actuator_control (0) #0,1,2,3
                    self.green_volt_control(0) #0 to 20
                    self.outer_led_control(0) #0 to 20
                    self.blue_led_Freq_control(0)   
                    self.all_led_off()
                    time.sleep(1)
                    self.actuator_control(1)    
                    time.sleep(3)
                self.all_led_off()
                self.on_time = 1
                self.actuator_control(1) 
                self.red_led_control(0) #0 to 20
                self.all_led_off()
                time.sleep(3)            
                self.blue_led_Freq_control(0)
                self.blue_led_volt_control(3,0) #0(0 to 19), 1(1 to 20), 2(1 to 20), 3(0 to 20)
                self.green_freq_control (16) # Flicker null value (0 to 15) and 16 = 0
                self.green_volt_control(20) #0 to 20
                self.inner_led_control(13) #0 to 20
                self.outer_led_control(20) #0 to 20
                self.actuator_control(1)    
                time.sleep(.5)
                if (self.on_time == 1):
                    time.sleep(1)
                self.blue_led_Freq_control(0) #0 to 250
                self.blue_led_volt_control(3,0) #0(0 to 19), 1(1 to 20), 2(1 to 20), 3(0 to 20)
                self.green_freq_control (0) # Flicker null value (0 to 15) and other 0
                self.green_volt_control(20) #0 to 20
                self.inner_led_control(13) #0 to 20
                self.outer_led_control(20) #0 to 20
                self.get_print('main_Prepair+++++++++++++')  
                self.green_led_on()  #check onec  
            self.back_flicker = 0     

        def flicker_Prepair (self):
            self.get_print('flicker_Prepair---------------------') 
            if (self.on_time == 1):
                self.green_led_on()
                self.back_flicker = 1
                self.blue_led_Freq_control(0) #0 to 250
                self.blue_led_volt_control(3,0) #0(0 to 19), 1(1 to 20), 2(1 to 20), 3(0 to 20)
                self.green_freq_control (0) # Flicker null value (0 to 15) and other 0
                self.green_volt_control(20) #0 to 20
                self.inner_led_control(13) #0 to 20
                self.outer_led_control(20) #0 to 20
                self.red_led_control(0) #0 to 20
            self.get_print('flicker_Prepair++++++++++++++++++') 


        def led_control(self, data_in):
            """
            Common LED control function for both inner and outer LEDs
            to ensure same brightness
            """
            if 0 <= data_in <= 20:
                dac_val = int(59.4 * data_in - 0.38095)
                # Control both LEDs with the same DAC value
                self.INNER_LED(dac_val)
                self.OUTER_LED(dac_val)
                str_data = f'LED_DAC = {dac_val} (Both Inner and Outer)'
                self.get_print(str_data)
            else:
                str_data = f'LED_DAC must be 0 to 20, invalid value: {data_in}'
                self.get_print(str_data)




        # def flicker_Prepair (self):
        #             self.all_led_off()
        #             self.actuator_control(1)
        #             time.sleep(1)
        #             self.all_led_off()
        #             self.outer_led_control(20) #0 to 20
        #             self.inner_led_control(13) #0 to 20            
        #             self.green_freq_control (0) # Flicker null value (0 to 15) and other 0
        #             self.green_volt_control(20) #0 to 20
        #             time.sleep(0.3)
        #             self.get_print('flicker_Prepair done')



        def cff_Fovea_Prepair (self):
            self.clr_pre_data()
            self.get_print('cff_Fovea--------------')     
            self.actuator_control(1)            
            if (self.on_time == 1):
                self.fliker_stop()
                self.red_led_control(0 ) #0 to 20
                self.blue_led_Freq_control(0 ) #0 to 250
                self.all_led_off()
                time.sleep(1)
                self.blue_led_Freq_control(0) #0 to 250
                self.blue_led_volt_control(3,0) #0(0 to 19), 1(1 to 20), 2(1 to 20), 3(0 to 20)
                self.green_freq_control (0) # Flicker null value (0 to 15) and other 0
                self.green_volt_control(20) #0 to 20
                self.inner_led_control(13) #0 to 20
                self.outer_led_control(20) #0 to 20
                self.red_led_control(0) #0 to 20
                time.sleep(1)
                self.fliker_start_g()
            self.get_print('cff_Fovea++++++++++++++') 

        def brk_Fovea_Prepair (self):
            self.get_print('brk_Fovea_Prepair--------------')    
            self.actuator_control(1)             
            if (self.on_time == 1):
                i = 20
                while i > 0:
                    self.blue_led_volt_control(1,i) #0(0 to 19), 1(1 to 20), 2(1 to 20), 3(0 to 20)
                    i -= 1
                    self.green_volt_control(i) #0 to 20
                    self.inner_led_control(i) #0 to 20
                    self.outer_led_control(i) #0 to 20
                    time.sleep(0.01)
                self.all_led_off()
                time.sleep(1)
                self.green_freq_control(0) # Flicker null value (0 to 15) and other 0
                self.green_volt_control(20) #0 to 20
                self.inner_led_control(13) #0 to 20
                self.outer_led_control(20) #0 to 20
                self.red_led_control(0) #0 to 20
                time.sleep(0.021)
                self.blue_led_Freq_control(160) #0 to 250
                self.blue_led_volt_control(0,0) #0(0 to 19), 1(1 to 20), 2(1 to 20), 3(0 to 20)
                self.red_led_control(0) #0 to 20
                self.fliker_start_b()
                self.fliker_Freq(self.get_cff_f_avg_cal())
            self.get_print('brk_Fovea_Prepair+++++++++++++') 


        def cff_Para_Fovea_Prepair (self):            
            self.get_print('cff_Para_Fovea_Prepair-----------') 
            if (self.on_time == 1):
                i = 20
                while i > 0:
                    self.blue_led_volt_control(2,i) #0(0 to 19), 1(1 to 20), 2(1 to 20), 3(0 to 20)
                    i -= 1
                    self.green_volt_control(i) #0 to 20
                    self.inner_led_control(i) #0 to 20
                    self.outer_led_control(i) #0 to 20
                    time.sleep(0.010)
                self.all_led_off()
#                 time.sleep(1.5)
                self.actuator_control(3) 
                time.sleep(5)
                self.actuator_control(2)                
                self.red_led_control(20) #0 to 20
                self.blue_led_Freq_control(11) #0 to 250
                self.blue_led_volt_control(3,0) #0(0 to 19), 1(1 to 20), 2(1 to 20), 3(0 to 20)
                self.green_freq_control(0) # Flicker null value (0 to 15) and other 0
                self.green_volt_control(20) #0 to 20
                self.inner_led_control(13) #0 to 20
                self.outer_led_control(20) #0 to 20
                self.fliker_start_b()
                time.sleep(4.5)
            self.get_print('cff_Para_Fovea_Prepair+++++++++++++++') 

        def brk_Para_Fovea_Prepair (self):
            self.get_print('brk_Para_Fovea_Prepair----------------') 
            self.actuator_control(2)
            if (self.on_time == 1):
                i = 20
                while i > 0:
                    self.blue_led_volt_control(2,i) #0(0 to 19), 1(1 to 20), 2(1 to 20), 3(0 to 20)
                    i -= 1
                    self.green_volt_control(i) #0 to 20
                    self.inner_led_control(i) #0 to 20
                    self.outer_led_control(i) #0 to 20
                    self.red_led_control(i) #0 to 20
                    time.sleep(0.050)
                self.all_led_off()
                time.sleep(4)
                self.green_freq_control(0) # Flicker null value (0 to 15) and other 0
                self.green_volt_control(20) #0 to 20
                self.inner_led_control(13) #0 to 20
                self.outer_led_control(20) #0 to 20
                self.red_led_control(20) #0 to 20
                self.blue_led_volt_control(3,20) #0(0 to 19), 1(1 to 20), 2(1 to 20), 3(0 to 20)
                self.blue_led_Freq_control(11) #0 to 250 
                time.sleep(0.050)                
                self.blue_led_volt_control(3,20) #0(0 to 19), 1(1 to 20), 2(1 to 20), 3(0 to 20)
                time.sleep(3)
                self.fliker_start_b()
                self.fliker_Freq(self.get_cff_p_avg_cal())
            self.get_print('brk_Para_Fovea_Prepair++++++++++++++++++++++') 

        def end_process (self):
            self.get_print('end_process---------------') 
            self.actuator_control(0)
            if (self.on_time == 1):
                i = 20
                while i > 0:
                    i -= 1
                    self.blue_led_volt_control(3,i) #0(0 to 19), 1(1 to 20), 2(1 to 20), 3(0 to 20)
                    self.green_volt_control(i) #0 to 20
                    self.inner_led_control(i) #0 to 20
                    self.outer_led_control(i) #0 to 20
                    self.red_led_control(i) #0 to 20
                    time.sleep(0.050)
                self.all_led_off()
                time.sleep(3)
            self.get_print('end_process++++++++') 
                

