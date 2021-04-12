import serial
import MySQLdb

dev = '/dev/ttyUSB0'

ser = serial.Serial(dev, 9600);

if __name__ == "__main__":
    print("Running serial_into_db.py")

    ser.flush()

    while 1:
        db = MySQLdb.connect("localhost", "pi", "", "hims_db") or die("Could not connect to database")

        while (ser.in_waiting == 0):
            pass

        line = ser.readline()
        tokens = line.split(":")
        nuid = tokens[0]
        weight = int(tokens[1])

        with db:
            cursor = db.cursor()

            cursor.execute("INSERT IGNORE INTO items (id, name) VALUES ('%s', '%s')" % (nuid, "Item Nil"))
            cursor.execute("INSERT INTO weights (item_id, weight) VALUES ('%s', %d)" % (nuid, weight))

            # Update status of item if weight passed threshold
            cursor.execute("UPDATE items SET state = IF(%s < threshold, 0, 1) WHERE id = '%s'" % (weight, nuid))

            db.commit()
            cursor.close()

        print("Insert into DB: (%s, %d)" % (nuid, weight))

