import json
import paho.mqtt.client as mqtt
import mysql.connector as mariadb

data_list = []

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/weather_station")
    client.subscribe("/control")
    
def on_message_weather_station(payload):
    data = json.loads(payload)
    dataID = data['id']
    temperature = data['temperature']
    humidity = data['humidity']
    wind_speed = data['wind_speed']
    wind_direction = data['wind_direction']
    pressure = data['pressure']
    time = data['time']
    if dataID < 5:
        print(dataID)
        global data_list
        data_list.append(list((temperature, humidity, wind_speed, wind_direction, pressure, time)))
        print(data_list)
    else:
        data_list.append(list((temperature, humidity, wind_speed, wind_direction, pressure, time)))
        print(dataID)
        print(data_list)
        mariadb_connection = mariadb.connect(host="Your IP", port=3306, user="Q", password="~~~", database="weather_station")
        print("已保存到数据库")
        cursor = mariadb_connection.cursor()
        sql = "INSERT INTO node_1 (temperature, humidity, wind_speed, wind_direction, pressure, time) VALUES (%s, %s, %s, %s, %s, %s)"
        try:
            cursor.executemany(sql, data_list)
            mariadb_connection.commit()
            mariadb_connection.close()
            data_list.clear()
        except mariadb.Error as error:
            print("Error: {}".format(error))
            
def on_message_control(payload):
    mariadb_connection = mariadb.connect(host="Your IP", port=3306, user="Q", password="~~~", database="weather_station")
    print(mariadb_connection)
    cursor = mariadb_connection.cursor()
    sql = "UPDATE settings SET running=%s WHERE id='1'"%(payload)
    try:
        cursor.execute(sql)
        mariadb_connection.commit()
        mariadb_connection.close()
    except mariadb.Error as error:
        print("Error: {}".format(error))
        
    
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if (msg.topic == "/weather_station"):
        #print(msg.topic+" "+str(msg.payload))
        on_message_weather_station(msg.payload)
    if (msg.topic == "/control"):
        on_message_control(msg.payload)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("Your IP", 1883, 60)
client.loop_forever()
