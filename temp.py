import RPi.GPIO as GPIO  
import itchat
import time  

itchat.auto_login(hotReload=True) 
                                 
@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    channel = 5            #pin 5  
    data = []           #temperature and humidity  
    j = 0               #counter  
  
    GPIO.setmode(GPIO.BCM)      #BCM mode  
  
    time.sleep(1)           #delay 1s 
  
    GPIO.setup(channel, GPIO.OUT)  
  
    GPIO.output(channel, GPIO.LOW)  
    time.sleep(0.02)        #remind the sensor to work 
    GPIO.output(channel, GPIO.HIGH)  
  
    GPIO.setup(channel, GPIO.IN)  
  
    while GPIO.input(channel) == GPIO.LOW:  
        continue  
  
    while GPIO.input(channel) == GPIO.HIGH:  
        continue  
  
    while j < 40:  
        k = 0  
        while GPIO.input(channel) == GPIO.LOW:  
            continue  
      
        while GPIO.input(channel) == GPIO.HIGH:  
            k += 1  
            if k > 100:  
                break  
      
        if k < 8:  
            data.append(0)  
        else:  
            data.append(1)  
  
        j += 1  
  
    print "sensor is working."  
    #print data                
  
    humidity_bit = data[0:8]        #divide into groups  
    humidity_point_bit = data[8:16]  
    temperature_bit = data[16:24]  
    temperature_point_bit = data[24:32]  
    check_bit = data[32:40]  

    humidity = 0  
    humidity_point = 0  
    temperature = 0  
    temperature_point = 0  
    check = 0  
  
    for i in range(8):  
        humidity += humidity_bit[i] * 2 ** (7 - i)              #trans to Decimal 
        humidity_point += humidity_point_bit[i] * 2 ** (7 - i)  
        temperature += temperature_bit[i] * 2 ** (7 - i)  
        temperature_point += temperature_point_bit[i] * 2 ** (7 - i)  
        check += check_bit[i] * 2 ** (7 - i)  
  
    tmp = humidity + humidity_point + temperature + temperature_point       #add Decimal datas 

    GPIO.setup(26,GPIO.IN)
    humi = str(humidity)
    temper = str(temperature)  
    checki = str(check)
    tmpi = str(tmp)
    if check == tmp:                                #check data, if equals than output  
        print "temperature : ", temperature, ", humidity : " , humidity 
        if GPIO.input(26) == 0: #detect if the light is on
            defaultReply = 'temperature: ' + temper + 'C humidity: ' + humi + '% light is ON'
        else :
            defaultReply = 'temperature: ' + temper + 'C humidity: ' + humi + '% light is OFF'
    else:                                       #ouput the wrong message  
        print "wrong"  
        print "temperature : ", temperature, ", humidity : " , humidity, " check : ", check, " tmp : ", tmp
        defaultReply = 'WRONG! Please try again. '    
    GPIO.cleanup()   
    return defaultReply
itchat.run()

