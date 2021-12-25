# encoding: utf-8
import json
import threading
import time
import paho.mqtt.client as mqtt
import requests
import pi_get_sensor_data as sensor
import sqlite3
import urllib
from urllib.request import urlopen

# 温度 湿度
import board
import busio
import adafruit_am2320

# 气压
import MS5611_Sensor

# 风速 风向
import wind_Sensor

isConnected = 1
isConnectedPrevious = 1
isConnectedOnBoot = 1
publishFlag = 1
dataID = 0

def is_internet():
    try:
        urlopen('http://www.baidu.com', timeout=1)
        return True
    except urllib.error.URLError as Error:
        return False

def get_running_status():
    global publishFlag
    temp = requests.get("https://Your IP/api/isRunning.php").json()
    publishFlag = int(temp[0]["running"])
    print("网络已连接")

def on_connect(client, userdata, flags, rc):
    print("Control connected with result code "+str(rc))
    
def on_message(client, userdata, msg):
    global publishFlag
    publishFlag = int(msg.payload)
    print(publishFlag)

def controlModual():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    client.connect("Your IP", 1883, 60)
    client.subscribe("/control")
    client.loop_forever()
    
def getData():
    global dataID
    if(dataID < 5):
        dataID += 1
    else:
        dataID = 1
        
    data = {}    
    data['id'] = dataID
    
    # 创建 i2c 总线
    i2c = busio.I2C(board.SCL, board.SDA)
    
    # 温度 湿度
    am2315 = adafruit_am2320.AM2320(i2c)
    data['temperature'] = am2315.temperature
    data['humidity'] = am2315.relative_humidity
    
    # 风向 风速
    wind = wind_Sensor.windSpeedandDirection()
    data['wind_speed'] = wind.speed
    data['wind_direction'] = wind.direction
    
    # 气压
    ms5611 = MS5611_Sensor.MS5611()
    data['pressure'] = ms5611.pressure
    
    # 时间
    data['time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #print(data)
    return json.dumps(data)     
    
def saveData(payload):
    data = json.loads(payload)
    temperature = data['temperature']
    humidity = data['humidity']
    wind_speed = data['wind_speed']
    wind_direction = data['wind_direction']
    pressure = data['pressure']
    time = data['time']
    
    conn = sqlite3.connect('weather_station.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO node_1 (temperature, humidity, wind_direction, wind_speed, pressure, time) VALUES (?, ?, ?, ?, ?, ?)", (temperature, humidity, wind_direction, wind_speed, pressure, time))
    conn.commit()
    conn.close()
    
def publishSavedModual():
    global dataID
    conn = sqlite3.connect('weather_station.db')
    cursor = conn.cursor()
    
    client = mqtt.Client()
    client.on_connect = on_connect
    
    cursor.execute("SELECT * FROM node_1")
    try:
        for row in cursor:
            if(dataID < 5):
                dataID += 1
            else:
                dataID = 1
            data = {}
            data['id'] = dataID
            data['time'] = row[0]
            data['temperature'] = row[1]
            data['humidity'] = row[2]
            data['wind_direction'] = row[3]
            data['wind_speed'] = row[4]
            data['pressure'] = row[5]
        
            client.connect("Your IP", 1883, 2)
            client.publish("/weather_station", json.dumps(data))
            time.sleep(0.5)
            print(data + "已发送。")
    except OSError as err:
        print("OS error: {0}".format(err))
    else:
        cursor.execute("DELETE FROM node_1")
        conn.commit()
    conn.close()
    
def publishModual(payload):
    global isConnected
    global isConnectedPrevious
    try:
        client = mqtt.Client()
        client.on_connect = on_connect
        client.connect("Your IP", 1883, 60)
        client.publish("/weather_station", payload)
        isConnectedPrevious = isConnected
        isConnected = 1
        print(payload + " 已发送。")
    except OSError as err:
        print("OS error: {0}".format(err))
        saveData(payload)
        isConnectedPrevious = isConnected
        isConnected = 0
    
if __name__ == '__main__':
    if is_internet():
        isConnectedOnBoot = 1
        get_running_status()
        threading.Thread(target = controlModual).start()
    else:
        isConnectedOnBoot = 0
    
    while True:
        if isConnected == 1 and isConnectedPrevious == 0:
            if isConnectedOnBoot == 0:
                isConnectedOnBoot = 0
                threading.Thread(target = controlModual).start()
            get_running_status()
            threading.Thread(target = publishSavedModual).start()
            
        if publishFlag == 1:
            time.sleep(5)
            threading.Thread(target = publishModual, args=(getData(),)).start()
