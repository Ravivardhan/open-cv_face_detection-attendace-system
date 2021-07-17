import cv2
import numpy as np
import face_recognition
import os
import datetime
import sqlite3
database=sqlite3.connect('face_recognizer')
cursor=database.cursor()

path = 'Training_images'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)
dict=dict()
for i in classNames:
    dict['{}'.format(i)]='absent'


def findEncodings(images):
    encodeList = []


    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnown = findEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            #print(name)
            if dict[classNames[matchIndex]]=='absent':
                dict[classNames[matchIndex]]='present'
            for i in dict:
                if dict[i] == 'present':
                    date = "".format(datetime.datetime.now().date())
                    time = "{}:{}:{}".format(datetime.datetime.now().hour, datetime.datetime.now().minute,
                                             datetime.datetime.now().second)
                    query = "select * from attendance where name='{}' and attendance='present'".format(i)
                    d = cursor.execute(query)
                    data_new = d.fetchall()
                    if len(data_new) >= 1:
                        pass
                    else:
                        cursor.execute("insert into attendance values('{}','{}','{}','{}')".format(i, dict[i],
                                                                                                   datetime.datetime.now().date(),
                                                                                                   time))
                        database.commit()
                        print("successfully stored")
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
print(dict)

cv2.destroyAllWindows()
