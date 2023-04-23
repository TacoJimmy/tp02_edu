import time
import serial
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu


def AC_PowerONOFF(PORT,ID,mode):
    try:
        master = modbus_rtu.RtuMaster(serial.Serial(port=PORT, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0))
        master.set_timeout(5.0)
        master.set_verbose(True)
        AC_status = master.execute(ID, cst.READ_HOLDING_REGISTERS, 0, 1)
        time.sleep(1)
        i = 0
        while AC_status[0] != mode and i < 5:
            master.execute(ID, cst.WRITE_SINGLE_REGISTER, 0, output_value=mode)
            time.sleep(1)
            AC_status = master.execute(ID, cst.READ_HOLDING_REGISTERS, 0, 1)
            time.sleep(1)
            i = i + 1
        return (AC_status[0])
        
    except:
        return ('loss_connect')
    
     
    
def AC_OPset(PORT,ID,mode): # Operaction  mode = (0=AC,1=humidi, 2=fan only) 
    try:
        master = modbus_rtu.RtuMaster(serial.Serial(port=PORT, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0))
        master.set_timeout(5.0)
        master.set_verbose(True)
        AC_OP = master.execute(ID, cst.READ_HOLDING_REGISTERS, 1, 1) 
        time.sleep(0.5)
        i = 0
        while AC_OP[0] != mode and i < 5:
            AC_OPValue = master.execute(ID, cst.WRITE_SINGLE_REGISTER, 1, output_value=mode)
            time.sleep(1)
            AC_OP = master.execute(ID, cst.READ_HOLDING_REGISTERS, 1, 1)
            i = i + 1
        master.close()
        return (AC_OP[0])
        
    except:
        master.close()
        return ('loss_connect')

def AC_FanSpeed(PORT,ID,mode): # mode = (0=auto,1~15 15=highest) 
    try:
        
        master = modbus_rtu.RtuMaster(serial.Serial(port=PORT, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0))
        master.set_timeout(5.0)
        master.set_verbose(True)
        AC_Fan = master.execute(ID, cst.READ_HOLDING_REGISTERS, 2, 1)
        time.sleep(0.5)
        i = 0
        if mode >=0 and mode<=15:
            while AC_Fan[0] != mode and i < 5:
                AC_FanValue = master.execute(ID, cst.WRITE_SINGLE_REGISTER, 2, output_value=mode)
                time.sleep(1)
                AC_Fan = master.execute(ID, cst.READ_HOLDING_REGISTERS, 2, 1)
                i = i + 1
        master.close()
        return (AC_Fan[0])
        
    except:
        master.close()
        return ('loss_connect')

def AC_SetTemp(PORT,ID,mode): # mode = temp
    try:
        
        master = modbus_rtu.RtuMaster(serial.Serial(port=PORT, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0))
        master.set_timeout(5.0)
        master.set_verbose(True)
        AC_settemp = master.execute(ID, cst.READ_HOLDING_REGISTERS, 3, 1)
        time.sleep(0.5)
        i = 0
        if mode <=30 and mode>=18:
            while AC_settemp[0] != mode and i < 5 :
                AC_settempvalue = master.execute(ID, cst.WRITE_SINGLE_REGISTER, 3, output_value=mode)
                time.sleep(1)
                AC_settemp = master.execute(ID, cst.READ_HOLDING_REGISTERS, 3, 1)
                i = i + 1
        master.close()
        return (AC_settemp[0])
        
    except:
        master.close()
        return ('loss_connect')

def AC_ReadHumi(PORT,ID):
    try:
        master = modbus_rtu.RtuMaster(serial.Serial(port=PORT, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0))
        master.set_timeout(5.0)
        master.set_verbose(True)
        AC_readhumid = master.execute(ID, cst.READ_HOLDING_REGISTERS, 1094, 1)
        AC_humid = AC_readhumid[0] * 0.01
        return (AC_humid)
    except:
        master.close()
        return ('loss_connect')

def AC_ReadOPTemp(PORT,ID): 
    try:
        
        master = modbus_rtu.RtuMaster(serial.Serial(port=PORT, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0))
        master.set_timeout(5.0)
        master.set_verbose(True)
        AC_readtemp = master.execute(ID, cst.READ_HOLDING_REGISTERS, 4, 1)
        time.sleep(0.5)
        
        master.close()
        return (AC_readtemp[0])
        
    except:
        master.close()
        return ('loss_connect')    
    
def AC_ReadSetTemp(PORT,ID): 
    try:
        
        master = modbus_rtu.RtuMaster(serial.Serial(port=PORT, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0))
        master.set_timeout(5.0)
        master.set_verbose(True)
        AC_readtemp = master.execute(ID, cst.READ_HOLDING_REGISTERS, 3, 1)
        time.sleep(0.5)
        master.close()
        return (AC_readtemp[0])
        
    except:
        master.close()
        return ('loss_connect')


def AC_ReadFullFunction(PORT,ID): # (value 0=on/off, 1=op mode, 2=fan speed, 3=set temp, 4=read temp)
    try:
        AC_infor = [0,0,0,0,0,0]
        if ID != 6:
            master = modbus_rtu.RtuMaster(serial.Serial(port=PORT, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0))
            master.set_timeout(5.0)
            master.set_verbose(True)
            AC_FullFunction = master.execute(ID, cst.READ_HOLDING_REGISTERS, 0, 5)
            time.sleep(0.2)
            AC_error = master.execute(ID, cst.READ_HOLDING_REGISTERS, 41, 1)
            time.sleep(0.2)
            AC_errorall = AC_error[0]
            AC_infor[0] = AC_FullFunction[0]
            AC_infor[1] = AC_FullFunction[1]
            AC_infor[2] = AC_FullFunction[2]
            AC_infor[3] = AC_FullFunction[3]
            AC_infor[4] = AC_FullFunction[4]
            AC_infor[5] = 1
            if AC_errorall == 1:
                AC_infor[5] = 0
        
            #master.close()
        else:
            AC_infor = [0,0,0,0,0,3]
        return (AC_infor)
    except:
        AC_infor[0] = 0
        AC_infor[1] = 0
        AC_infor[2] = 0
        AC_infor[3] = 0
        AC_infor[4] = 0
        AC_infor[5] = 2
        #master.close()
        return (AC_infor)

def AC_error(PORT,ID): # (value 0=on/off, 1=op mode, 2=fan speed, 3=set temp, 4=read temp)
    AC_infor = [0,0,0,0,0,0]
    
    master = modbus_rtu.RtuMaster(serial.Serial(port=PORT, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0))
    master.set_timeout(5.0)
    master.set_verbose(True)
            
            
    AC_error = master.execute(ID, cst.READ_HOLDING_REGISTERS, 514, 1)
    return AC_error        

def AC_TrunONOFF(PORT, ID, mode):
    AC_CtrlStatus = AC_PowerONOFF(PORT,ID,mode)
    if AC_CtrlStatus == 'loss_connect' :
        i = 0
        while (AC_CtrlStatus == "loss_connect") and (i < 5) :
            AC_CtrlStatus = AC_PowerONOFF(PORT,ID,mode)
            i = i + 1
            time.sleep(.5)
    return ('done')

def AC_TrunMode(PORT, ID, mode):
    AC_CtrlStatus = AC_OPset(PORT,ID,mode)
    if AC_CtrlStatus == 'loss_connect' :
        i = 0
        while (AC_CtrlStatus == "loss_connect") and (i < 5) :
            AC_CtrlStatus = AC_OPset(PORT,ID,mode)
            i = i + 1
            time.sleep(.5)
    return ('done')

def AC_TrunTemp(PORT, ID, mode):
    AC_CtrlStatus = AC_SetTemp(PORT,ID,mode)
    if AC_CtrlStatus == 'loss_connect' :
        i = 0
        while (AC_CtrlStatus == "loss_connect") and (i < 5) :
            AC_CtrlStatus = AC_SetTemp(PORT,ID,mode)
            i = i + 1
            time.sleep(.5)
    return ('done')

if __name__ == '__main__':
    while True:
        #print (AC_TrunONOFF('/dev/ttyS1', 123, 0))
        '''
        print (AC_TrunONOFF('/dev/ttyS1', 123, 1))
        print (AC_TrunMode('/dev/ttyS1', 123, 0))
        print (AC_TrunTemp('/dev/ttyS1', 123, 26))
        '''
        
        print (AC_ReadFullFunction('/dev/ttyS1',123))
        
        
        time.sleep(5)
