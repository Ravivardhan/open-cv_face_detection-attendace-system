import sqlite3
import datetime
import pandas
print("{}:{}:{}".format(datetime.datetime.now().hour,datetime.datetime.now().minute,datetime.datetime.now().second))
database=sqlite3.connect('face_recognizer')
cursor=database.cursor()

#cursor.execute('create table attendance(name varchar(20),attendance varchar(20),date varchar(20),time varchar(20))')
#cursor.execute('alter table attendance rename column attendace to attendance')


data=cursor.execute("select * from attendance")
data=(data.fetchall())
pandas.set_option("display.max_rows",None,"display.max_columns",None)
df=pandas.DataFrame(data,columns=['name','attendance','date','time'])
print(df)


database.commit()