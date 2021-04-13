import tkinter as tk
from tkinter import Message ,Text
import cv2,os
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
from tkinter import messagebox
import tkinter.ttk as ttk
import tkinter.font as font

window = tk.Tk()
#helv36 = tk.Font(family='Helvetica', size=36, weight='bold')
window.title("FACE ATTENDENCE")

dialog_title = 'QUIT'
dialog_text = 'Are you sure?'
# answer = messagebox.askquestion(dialog_title, dialog_text)
 
# window.geometry('1280x720')
window.configure(background='white')

window.attributes('-fullscreen', True)

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)




message = tk.Label(window, text="Face-Recognition-Based-Attendance-Management-System" ,bg="blue"  ,fg="white"  ,width=50  ,height=3,font=('caliber', 30, 'bold')) 

message.place(x=200, y=20)

lbl = tk.Label(window, text="Enter ID",width=20  ,height=2  ,fg="white"  ,bg="blue" ,font=('times', 15, ' bold ') ) 
lbl.place(x=400, y=200)

txt = tk.Entry(window,width=20  ,bg="blue" ,fg="white",font=('times', 15, ' bold '))
txt.place(x=700, y=215)

lbl2 = tk.Label(window, text="Enter Name",width=20  ,fg="white"  ,bg="blue"    ,height=2 ,font=('times', 15, ' bold ')) 
lbl2.place(x=400, y=300)

txt2 = tk.Entry(window,width=20  ,bg="blue"  ,fg="white",font=('times', 15, ' bold ')  )
txt2.place(x=700, y=315)

lbl31 = tk.Label(window, text="New Student? click to register ",width=30  ,fg="white"  ,bg="blue"  ,height=2 ,font=('times', 15, ' bold underline ')) 
lbl31.place(x=200, y=650)

lbl3 = tk.Label(window, text="Notification : ",width=20  ,fg="white"  ,bg="blue"  ,height=2 ,font=('times', 15, ' bold underline ')) 
lbl3.place(x=800, y=770)

message = tk.Label(window, text="" ,bg="blue"  ,fg="white"  ,width=30  ,height=2, activebackground = "blue" ,font=('times', 15, ' bold ')) 
message.place(x=1100, y=770)

lbl3 = tk.Label(window, text="Attendance : ",width=20  ,fg="white"  ,bg="blue"  ,height=2 ,font=('times', 15, ' bold  underline')) 
lbl3.place(x=400, y=400)


message2 = tk.Label(window, text="" ,fg="red"   ,bg="blue",activeforeground = "green",width=30  ,height=2  ,font=('times', 15, ' bold ')) 
message2.place(x=700, y=400)
 
def clear():
    txt.delete(0, 'end')    
    res = ""
    message.configure(text= res)

def clear2():
    txt2.delete(0, 'end')    
    res = ""
    message.configure(text= res)    
    
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False
 
def TakeImages():        
    Id=(txt.get())
    name=(txt2.get())
    if(is_number(Id) and name.isalpha()):
        cam = cv2.VideoCapture(0)
        #TrainingImage
        harcascadePath = "C:\\Users\\WhysoseriousONI\\Desktop\\Face-Recognition-Based-Attendance-System-master\\haarcascade_frontalface_default.xml"
        detector=cv2.CascadeClassifier(harcascadePath)
        sampleNum=0
        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
               
                sampleNum=sampleNum+1
                
                cv2.imwrite("C:\\Users\\WhysoseriousONI\\Desktop\\Face-Recognition-Based-Attendance-System-master\\TrainingImage\\ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                
                cv2.imshow('frame',img)
            
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            
            elif sampleNum>150:
                break
        cam.release()
        cv2.destroyAllWindows() 
        res = "Images Saved for ID : " + Id +" Name : "+ name
        row = [Id , name]
        with open('C:\\Users\\WhysoseriousONI\\Desktop\\Face-Recognition-Based-Attendance-System-master\\StudentDetails\\StudentDetails.csv','a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message.configure(text= res)
    else:
        if(is_number(Id)):
            res = "Enter Alphabetical Name"
            message.configure(text= res)
        if(name.isalpha()):
            res = "Enter Numeric Id"
            message.configure(text= res)
    


def Train_and_replace():
    #os.remove("C:\\Users\\WhysoseriousONI\\Desktop\\Face-Recognition-Based-Attendance-System-master\\TrainingImage\\Trainner.yml")
    recognizer = cv2.face.LBPHFaceRecognizer_create()#recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
    harcascadePath = "C:\\Users\\WhysoseriousONI\\Desktop\\Face-Recognition-Based-Attendance-System-master\\haarcascade_frontalface_default.xml"
    detector =cv2.CascadeClassifier(harcascadePath)
    faces,Id = getImagesAndLabels("C:\\Users\\WhysoseriousONI\\Desktop\\Face-Recognition-Based-Attendance-System-master\\TrainingImage")
    recognizer.train(faces, np.array(Id))
    recognizer.save("C:\\Users\\WhysoseriousONI\\Desktop\\Face-Recognition-Based-Attendance-System-master\\TrainingImage\\Trainner.yml")
    res = "Image Trained"#+",".join(str(f) for f in Id)
    message.configure(text= res)

def TrainImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()#recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
    harcascadePath = "C:\\Users\\WhysoseriousONI\\Desktop\\Face-Recognition-Based-Attendance-System-master\\haarcascade_frontalface_default.xml"
    detector =cv2.CascadeClassifier(harcascadePath)
    faces,Id = getImagesAndLabels("C:\\Users\\WhysoseriousONI\\Desktop\\Face-Recognition-Based-Attendance-System-master\\TrainingImage")
    recognizer.train(faces, np.array(Id))
    recognizer.save("C:\\Users\\WhysoseriousONI\\Desktop\\Face-Recognition-Based-Attendance-System-master\\TrainingImage\\Trainner.yml")
    res = "Image Trained"#+",".join(str(f) for f in Id)
    message.configure(text= res)

def getImagesAndLabels(path):
    
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    #print(imagePaths)
    
    
    faces=[]
    
    Ids=[]
  
    for imagePath in imagePaths:
        
        pilImage=Image.open(imagePath).convert('L')
        
        imageNp=np.array(pilImage,'uint8')
        
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        
        faces.append(imageNp)
        Ids.append(Id)        
    return faces,Ids

def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()#cv2.createLBPHFaceRecognizer()
    recognizer.read("C:\\Users\\WhysoseriousONI\\Desktop\\Face-Recognition-Based-Attendance-System-master\\TrainingImage\\Trainner.yml")
    harcascadePath = "C:\\Users\\WhysoseriousONI\\Desktop\\Face-Recognition-Based-Attendance-System-master\\haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);    
    df=pd.read_csv("C:\\Users\\WhysoseriousONI\\Desktop\\Face-Recognition-Based-Attendance-System-master\\StudentDetails\\StudentDetails.csv")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX        
    col_names =  ['Id','Name','Date','Time']
    attendance = pd.DataFrame(columns = col_names)    
    while True:
        ret, im =cam.read()
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray, 1.2,5)    
        for(x,y,w,h) in faces:
            cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w])                                   
            if(conf < 50):
                ts = time.time()      
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa=df.loc[df['Id'] == Id]['Name'].values
                tt=str(Id)+"-"+aa
                attendance.loc[len(attendance)] = [Id,aa,date,timeStamp]
                
            else:
                Id='Unknown'                
                tt=str(Id)  
                        
            cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)        
        attendance=attendance.drop_duplicates(subset=['Id'],keep='first')    
        cv2.imshow('im',im) 
        if (cv2.waitKey(1)==ord('q')):
            break
    ts = time.time()      
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour,Minute,Second=timeStamp.split(":")
    fileName="C:\\Users\\WhysoseriousONI\\Desktop\\Face-Recognition-Based-Attendance-System-master\\Attendance\\Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
    attendance.to_csv(fileName,index=False)
    cam.release()
    cv2.destroyAllWindows()
    #print(attendance)
    res=attendance
    message2.configure(text= res)

  
clearButton = tk.Button(window, text="Clear", command=clear  ,fg="white"  ,bg="blue"  ,width=20  ,height=2 ,activebackground = "white" ,font=('times', 15, ' bold '))
clearButton.place(x=950, y=200)
clearButton2 = tk.Button(window, text="Clear", command=clear2  ,fg="white"  ,bg="blue"  ,width=20  ,height=2, activebackground = "white" ,font=('times', 15, ' bold '))
clearButton2.place(x=950, y=300)    
takeImg = tk.Button(window, text="Capture", command=TakeImages  ,fg="white"  ,bg="blue"  ,width=20  ,height=3, activebackground = "white" ,font=('times', 15, ' bold '))
takeImg.place(x=200, y=750)
trainImg = tk.Button(window, text="For new student", command=Train_and_replace  ,fg="white"  ,bg="blue"  ,width=20  ,height=3, activebackground = "white" ,font=('times', 15, ' bold ')) #trainimages
trainImg.place(x=500, y=750)
trackImg = tk.Button(window, text="Take Attendances", command=TrackImages  ,fg="white"  ,bg="blue"  ,width=20  ,height=3, activebackground = "white" ,font=('times', 15, ' bold '))
trackImg.place(x=650, y=500)
quitWindow = tk.Button(window, text="Quit", command=window.destroy  ,fg="white"  ,bg="blue"  ,width=20  ,height=3, activebackground = "white" ,font=('times', 15, ' bold '))
quitWindow.place(x=1200, y=500)

def exit(event):
    window.destroy()

window.bind("<Escape>", exit)


window.mainloop()