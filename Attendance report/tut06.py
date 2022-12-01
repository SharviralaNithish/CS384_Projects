#I HAVE USED GMAIL, ENABLE 2 STEP VERIFICATION AND USE AUTHENTICATION GENERATED PASSWORD AS PASSWORD.
#We are using datetime library to find out duration of the runtime of the program
from datetime import datetime
start_time=datetime.now()
try:
    #Here we are importing pandas library because we are working on excel spreadsheet(Excel spreadsheet is same as pandas dataframe)
    #Numpy helps us to perform various mathematical operations
    #We are using calendar library to find out the day of a particular date
    import pandas as pd
    import numpy as np
    from datetime import datetime
    from datetime import timedelta
    import calendar
    import sys
    import time
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    #This function generates the Attendance report
    #Output will be in consolidated form as well as individual form 
    def attendance_report():
        input_file = pd.read_csv("input_registered_students.csv")
        data = input_file.copy()
        input_file2 = pd.read_csv("input_attendance.csv")
        data2 = input_file2.copy()
        rollnum=list(data["Roll No"])
        registerednames=list(data["Name"])
        attendance=list(data2["Attendance"])
        z=list(data2["Timestamp"])
        x=data2["Timestamp"][0]
        y=data2["Timestamp"][len(data2)-1]
 #   print(y)
    #x="28-07-2022"
        yearstart=x[6:10]
        monstart=x[3:5]
        datestart=x[0:2]
        datfor=yearstart+"-"+monstart+"-"+datestart
        monthur=calendar.weekday(int(yearstart),int(monstart),int(datestart))
        begindate=datetime.strptime(datfor,"%Y-%m-%d")
        yearend=y[6:10]
        monend=y[3:5]
        dateend=y[0:2]
        datfor1=yearend+"-"+monend+"-"+dateend
        begindate1=datetime.strptime(datfor1,"%Y-%m-%d")
        i=0
        l=[x]
        while(i==0):
            if(monthur==0):
                begindate=begindate+timedelta(days=3)
            # l.append(begindate)
                p=str(begindate)
                yea=p[0:4]
                mon=p[5:7]
                da=p[8:10]
                monthur=calendar.weekday(int(yea),int(mon),int(da))
                appe=da+"-"+mon+"-"+yea
                if(appe[6:10]==y[6:10]):
                    if((mon==y[3:5])):
                        if(int(da)>=int(y[0:2])):
                            l.append(appe)
                            i=1
                        else:
                            l.append(appe)
                    elif(int(mon)<int(y[3:5])):
                        l.append(appe)
                    else:
                        i=1
                else:
                    i=1
            elif(monthur==3):
                begindate=begindate+timedelta(days=4)
            # l.append(begindate)
                p=str(begindate)
                yea=p[0:4]
                mon=p[5:7]
                da=p[8:10]
                monthur=calendar.weekday(int(yea),int(mon),int(da))
                appe=str(da)+"-"+str(mon)+"-"+str(yea)
                #l.append(appe)
                #print(begindate)
                if(appe[6:10]==y[6:10]):
                    if((mon==y[3:5])):
                        if(int(da)>=int(y[0:2])):
                            l.append(appe)
                            i=1
                        else:
                            l.append(appe)
                    elif(int(mon)<int(y[3:5])):
                        l.append(appe)
                    else:
                        i=1
                else:
                    i=1
        for i in range(1,len(l)+1):
            dateforcol="Date "+str(i)
            data[dateforcol]=""
        totcls=[len(l)]*(data.shape[0])
        data["Total Lecture Taken"]=totcls
        data["Total Real"]=""
        data["Attendance"]=" "
        for i in range(0,len(rollnum)):
            attcheck=[]
            for j in range(0,len(attendance)):
                if(rollnum[i]==str(attendance[j])[0:8]):
                    attcheck.append(z[j])
       # print(attcheck)
            attendedclasses=0
            for k in range(0,len(l)):
                s=0
                a=0
                for m in range(0,len(attcheck)):
                    if(l[k]==attcheck[m][0:10]):
                        da=attcheck[m][0:2]
                        mon=attcheck[m][3:5]
                        yea=attcheck[m][6:10]
                        hou=attcheck[m][11:13]
                        minu=attcheck[m][14:16]
                        sec=attcheck[m][17:19]
                        if(hou=="14"):
                            if(a==0):
                                a=a+1
                                data.iloc[i,k+2]="P"
                                attendedclasses=attendedclasses+1
                        else:
                            data.iloc[i,k+2]="A"
                attr=[]
                for q in attcheck:
                    attr.append(q[0:10])
                for k in range(0,len(l)):
                    if(l[k] in attr):
                        continue
                    else:
                        data.iloc[i,k+2]="A"
            data["Total Real"][i]=attendedclasses
            x=round(float((attendedclasses/len(l))*100),2)
            # print(x)
            data["Attendance"][i]=x
        fla=[" "]
        for i in range(1,len(l)+1):
            fla.append("Date "+str(i))
        #In this loop we gonna generate the individual student attendance report
        for i in range(0,len(rollnum)):
            df=pd.DataFrame([])
            df["Date"]=fla
            df["Roll"]=""
            df["Roll"][0]=rollnum[i]
            df["Name"]=""
            df["Name"][0]=registerednames[i]
            df["Total Attendance Count"]=""
            df["Real"]=""
            df["Duplicate"]=""
            df["Invalid"]=""
            df["Absent"]=""
            tot=0
            attcheck=[]
            for j in range(0,len(attendance)):
                if(rollnum[i]==str(attendance[j])[0:8]):
                    attcheck.append(z[j])
                    tot=tot+1
            duptot=0
            realtot=0
            invtot=0
            for k in range(0,len(l)):
                totper=0
                s=0
                a=0
                dup=0
                inv=0
                for m in range(0,len(attcheck)):
                    if(l[k][0:10]==attcheck[m][0:10]):
                        da=attcheck[m][0:2]
                        mon=attcheck[m][3:5]
                        yea=attcheck[m][6:10]
                        hou=attcheck[m][11:13]
                        minu=attcheck[m][14:16]
                        sec=attcheck[m][17:19]
                        totper=totper+1
                        if(hou=="14"):
                            if(a==0):
                                a=a+1
                            else:
                                dup=dup+1
                        else:
                            inv=inv+1
                duptot=duptot+dup
                realtot=realtot+a
                invtot=invtot+inv
                df["Real"][k+1]=a
                df["Duplicate"][k+1]=dup
                df["Total Attendance Count"][k+1]=totper
                df["Invalid"][k+1]=inv
                if(a==1):
                    df["Absent"][k+1]=0
                else:
                    df["Absent"][k+1]=1
            df["Total Attendance Count"][0]=tot
            df["Duplicate"][0]=duptot
            df["Real"][0]=realtot
            df["Invalid"][0]=invtot
            df["Absent"][0]=(len(l)-realtot)
            filename="output/"+rollnum[i]+".xlsx"
            #The below line converts our dataframe in to an excel format file in individual format
            df.to_excel(filename,index=False)
        #The below line converts the dataframe in to an excel format file in consolidated form          
        data.to_excel("output/attendance_report_consolidated.xlsx",index=False)
        #here add your gmail email-adress.
        fromaddr = "nithish277@gmail.com"
        #add the sender's gmail adress.
        toaddr = "nithishsharvirala23@gmail.com"
   
# instance of MIMEMultipart
        msg = MIMEMultipart()

#here i am storing the sender's email and receivers email address
        msg['From'] = fromaddr
        msg['To'] = toaddr
  
# storing the subject 
        msg['Subject'] = "Tut 06 attendance_report_consolidated file"
  
#here i am storing the body of the mail,in the string.
        body = "here is the file"
  
# attach the body with the msg instance
        msg.attach(MIMEText(body, 'plain'))
  
# add the file name with the extension here which you want to sent.
        filename = "attendance_report_consolidated.xlsx"
        attachment = open("output/attendance_report_consolidated.xlsx", "rb")
  
# instance of MIMEBase and named as p
        p = MIMEBase('application', 'octet-stream')
  
# To change the payload into encoded form
        p.set_payload((attachment).read())
  
# encode into base64
        encoders.encode_base64(p)
   
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(p)
  
        s = smtplib.SMTP('smtp.gmail.com', 587)
  
# for security purpose start the tls.
        s.starttls()
  
#here use your email adress, and authenication password.
        s.login(fromaddr, "hqwsktscesjqmbdd")
  
#now convert multipart msg into the string.
        text = msg.as_string()
  
# here i am sending the email..by representing fromaddr, toaddr, text.
        s.sendmail(fromaddr, toaddr, text)
  
#quitting the session atlast.
        s.quit()
    attendance_report()
except:
    print("File has some error")

#The below lines of code helps us to know the duration of runtime of this program
end_time=datetime.now()
print(start_time)
print(end_time)
print(end_time-start_time)                    