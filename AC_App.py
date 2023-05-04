# coding:utf-8
import codecs
import json
import ssl
import paho.mqtt.client as mqtt
import time
import AC_Ctrl
import threading
import time
import schedule  



def on_connect(client, userdata, flags, rc):
    print("Connected with result code"+str(rc))
    client.subscribe('v1/devices/me/rpc/request/+',1)
    time.sleep(3)

def ipcaccontrl(data_payload):
    print (data_payload)
    print (data_payload['params'])
    
    
    if data_payload['method'] == 'AC1_SetOnOff':
        if data_payload['params'] == False:
            AC_Ctrl.AC_TrunONOFF('/dev/ttyS1', 123, 0)
            
        
        if data_payload['params'] == True:
            AC_Ctrl.AC_TrunONOFF('/dev/ttyS1', 123, 1)
    if data_payload['method'] == 'AC1_SetTemp':
        AC_Ctrl.AC_TrunTemp('/dev/ttyS1', 123, data_payload['params'])
        
    if data_payload['method'] == 'AC2_SetOnOff':
        if data_payload['params'] == False:
            AC_Ctrl.AC_TrunONOFF('/dev/ttyS1', 155, 0)
        
        if data_payload['params'] == True:
            AC_Ctrl.AC_TrunONOFF('/dev/ttyS1', 155, 1)
    if data_payload['method'] == 'AC2_SetTemp':
        AC_Ctrl.AC_TrunTemp('/dev/ttyS1', 155, data_payload['params'])
        
    if data_payload['method'] == 'AC3_SetOnOff':
        if data_payload['params'] == False:
            AC_Ctrl.AC_TrunONOFF('/dev/ttyS1', 156, 0)
        
        if data_payload['params'] == True:
            AC_Ctrl.AC_TrunONOFF('/dev/ttyS1', 156, 1)
    if data_payload['method'] == 'AC3_SetTemp':
        AC_Ctrl.AC_TrunTemp('/dev/ttyS1', 156, data_payload['params'])
        
    if data_payload['method'] == 'AC4_SetOnOff':
        if data_payload['params'] == False:
            AC_Ctrl.AC_TrunONOFF('/dev/ttyS1', 157, 0)
        
        if data_payload['params'] == True:
            AC_Ctrl.AC_TrunONOFF('/dev/ttyS1', 157, 1)
    if data_payload['method'] == 'AC4_SetTemp':
        AC_Ctrl.AC_TrunTemp('/dev/ttyS1', 157, data_payload['params'])
            
            
def on_message(client, userdata, msg):
    data_topic = msg.topic
    data_payload = json.loads(msg.payload.decode())
    time.sleep(.5)
    listtopic = data_topic.split("/")  
    signal_fb = 'v1/devices/me/rpc/response/'+str(listtopic[5]) # response topic
    
    fb_payload = ipcaccontrl(data_payload)
    
    client.publish(signal_fb,json.dumps(fb_payload)) # send response


def ipc_subscribe():
    try:
        meter_token = 'fjfp5i9VxcPRC7FrChr0'
        meter_pass = ''
        url = 'thingsboard.cloud'

        client = mqtt.Client('', True, None)
        client.on_connect = on_connect
        time.sleep(.5)
        client.on_message = on_message
        time.sleep(.5)
        client.username_pw_set(meter_token, meter_pass)
        client.connect(url, 1883, 60)


        client.loop_forever()
    except:
        pass

def AC_Infor():
    try:
        meter_token = 'k6XyHLptVPFxXgrT7tm5'
        meter_pass = ''
        url = 'thingsboard.cloud'

        client1 = mqtt.Client('', True, None)
        client1.username_pw_set(meter_token, meter_pass)
        client1.connect(url, 1883, 60)
        time.sleep(1)
    
        #AC1
        AC1_Infor = AC_Ctrl.AC_ReadFullFunction('/dev/ttyS1',123)
        if AC1_Infor[5] == 2:
            AC1_Infor = AC_Ctrl.AC_ReadFullFunction('/dev/ttyS1',123)
        payload = {'AC1_Status' : AC1_Infor[0],
                    'AC1_mode':AC1_Infor[1],
                    'AC1_windspeed':AC1_Infor[2],
                    'AC1_settemp':AC1_Infor[3],
                    'AC1_roomtemp':AC1_Infor[4],
                    'AC1_linkinfor':AC1_Infor[5] 
                    }
        print (json.dumps(payload))
        if AC1_Infor[5] != 2:
            client1.publish('v1/devices/me/telemetry', json.dumps(payload))
            time.sleep(5)
        #AC2
        AC2_Infor = AC_Ctrl.AC_ReadFullFunction('/dev/ttyS1',155)
        if AC2_Infor[5] == 2:
            AC2_Infor = AC_Ctrl.AC_ReadFullFunction('/dev/ttyS1',155)
        payload = {'AC2_Status' : AC2_Infor[0],
                'AC2_mode':AC2_Infor[1],
                'AC2_windspeed':AC2_Infor[2],
                'AC2_settemp':AC2_Infor[3],
                'AC2_roomtemp':AC2_Infor[4],
                'AC2_linkinfor':AC2_Infor[5] }
        print (json.dumps(payload))
        if AC2_Infor[5] != 2:
            client1.publish('v1/devices/me/telemetry', json.dumps(payload))
            time.sleep(5)
        #AC3
        AC3_Infor = AC_Ctrl.AC_ReadFullFunction('/dev/ttyS1',156)
        if AC3_Infor[5] == 2:
            AC3_Infor = AC_Ctrl.AC_ReadFullFunction('/dev/ttyS1',156)
        payload = {'AC3_Status' : AC3_Infor[0],
                'AC3_mode':AC3_Infor[1],
                'AC3_windspeed':AC3_Infor[2],
                'AC3_settemp':AC3_Infor[3],
                'AC3_roomtemp':AC3_Infor[4],
                'AC3_linkinfor':AC3_Infor[5] }
        print (json.dumps(payload))
        if AC3_Infor[5] != 2:
            client1.publish('v1/devices/me/telemetry', json.dumps(payload))
            time.sleep(5)
        #AC4
        AC4_Infor = AC_Ctrl.AC_ReadFullFunction('/dev/ttyS1',157)
        if AC4_Infor[5] == 2:
            AC4_Infor = AC_Ctrl.AC_ReadFullFunction('/dev/ttyS1',157)
        payload = {'AC4_Status' : AC4_Infor[0],
                'AC4_mode':AC4_Infor[1],
                'AC4_windspeed':AC4_Infor[2],
                'AC4_settemp':AC4_Infor[3],
                'AC4_roomtemp':AC4_Infor[4],
                'AC4_linkinfor':AC4_Infor[5] }
        print (json.dumps(payload))
        if AC4_Infor[5] != 2:
            client1.publish('v1/devices/me/telemetry', json.dumps(payload))
            time.sleep(5)
    except:
        pass

schedule.every(30).seconds.do(AC_Infor)
 
t = threading.Thread(target=ipc_subscribe)
t.start()
    
    
if __name__ == '__main__':
    while True:  
        schedule.run_pending()  
        time.sleep(1)  
    
