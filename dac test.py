from dac_lib_soft import mup4728
import time
dac = mup4728(0x61)
# 
# data = [136,136,135,135,134]
# dac.put_brk_fovea_min(data)
# data = [159,158,158,158,158]
# dac.put_brk_fovea_mid(data)
# data = [184,182,181,181,181]
# dac.put_brk_fovea_max(data)
# 
# dac.put_blue_volt_nul(2)
# 
# data = [7,6,5,5,5]
# dac.put_brk_para_f_min(data)
# data = [30,29,29,29,29]
# dac.put_brk_para_f_mid(data)
# data = [55,54,53,53,53]
# dac.put_brk_para_f_max(data)
# 
# 
# 
# dac.get_cal_f_mpod()
# dac.get_cal_f_sd()



# dac.get_cff_f_min_cal(0,12.0)
# dac.get_cff_f_min_cal(1, 12.5)
# dac.get_cff_f_min_cal(2, 13.0)
# dac.get_cff_f_min_cal(3, 13.8)
# dac.get_cff_f_min_cal(4,13.6)
# dac.get_cff_f_max_cal()
# dac.get_cff_f_avg_cal()
# dac.cff_Para_Fovea_Prepair()
# dac.buzzer_on()
# dac.buzzer_1()
# dac.buzzer_3()
# dac.actuator_control(2)        
# dac.blue_led_Freq_control(160) #0 to 250
# dac.blue_led_volt_control(0,3) #0(0 to 19), 1(1 to 20), 2(1 to 20), 3(0 to 20)
# dac.green_freq_control(0) # Flicker null value (0 to 15) and other 0
# dac.green_volt_control(20) #0 to 20
# dac.inner_led_control(20) #0 to 20
# dac.outer_led_control(20) #0 to 20                
# dac.fliker_start_b()
# dac.fliker_Freq(27.78)
# dac.red_led_control(0) #0 to 20
# dac.main_Prepair()
# dac.fan_on()
# dac.buzzer_3()
# # time.sleep(5)
# dac.all_led_off()
# dac.main_Prepair()
# print("main_Prepair")
# dac.buzzer_1()
# time.sleep(5)
# dac.all_led_off()
# dac.flicker_Prepair()
# print("flicker_Prepair")
# dac.buzzer_1()
# time.sleep(5)
# dac.all_led_off()
# dac.cff_Fovea_Prepair()
# print("cff_Fovea_Prepair")
# dac.buzzer_1()
# time.sleep(5)
# dac.all_led_off()
# dac.brk_Fovea_Prepair()
# print("brk_Fovea_Prepair")
# dac.buzzer_1()
# time.sleep(5)
# dac.all_led_off()
dac.on_time = 1
# dac.cff_Para_Fovea_Prepair()
# print("cff_Para_Fovea_Prepair")
# dac.buzzer_1()
# time.sleep(5)
dac.all_led_off()
dac.put_cff_p_avg_cal(19.5)
dac.brk_Para_Fovea_Prepair()

print("brk_Para_Fovea_Prepair")
while(1):    
    dac.buzzer_3()
    time.sleep(1)
#     dac.buzzer_on()
# #     time.sleep(1)
# #     dac.buzzer_off()#D4 Buzz
    
    
#  dac.green_volt_control(20) #0 to 20
# dac.green_freq_control(15) # Flicker null value (0 to 15) and other 0
# dac.inner_led_control(20) #0 to 20
# dac.outer_led_control(20) #0 to 20
# dac.red_led_control(20) #0 to 20
# dac.fliker_Freq(30.2)
# dac.fliker_start_b()
# # dac.fliker_Freq(10)
# # dac.green_led_off()
# # dac.blue_led_on()
# dac.buzzer_3()
# while(1):
#     a=1

