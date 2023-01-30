import MySQLdb

def dataPush(ty):
    db = MySQLdb.connect(host='localhost',user='piuser',password='123456',database='asfalis')
    cur = db.cursor()
    if (ty==1):
        cur.execute("INSERT INTO SensorData (`id`, sensor, location, value) VALUES ('1', 'flame', 'Kitchen', 'a')")  
    elif(ty==2):
        cur.execute("INSERT INTO SensorData (`id`, sensor, location, value) VALUES ('2', 'Ultrasonic', 'Hallway', 'a')")
    elif(ty==3):
        cur.execute("INSERT INTO SensorData (`id`, sensor, location, value) VALUES ('3', 'Dorr', 'Entrance', 'a')")
    elif(ty==4):
        cur.execute("INSERT INTO SensorData (`id`, sensor, location, value) VALUES ('4', 'PIR Sensor', 'Living room', 'a')")     
    else:
        cur.execute("INSERT INTO SensorData (`id`, sensor, location, value) VALUES ('5', 'Smoke Sensor', 'Kitchen', 'a')")   
       
    db.commit()
