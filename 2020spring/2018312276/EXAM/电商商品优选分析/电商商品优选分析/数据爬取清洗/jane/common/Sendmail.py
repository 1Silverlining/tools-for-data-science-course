# -*- coding: utf-8 -*-
'''
send mail
'''
import smtplib
from email.MIMEText import MIMEText

_to=['lianpengtao@leying365.com'] #,
_host='smtp.exmail.qq.com'
_user='nb_monit@leying365.com'
_pass="lyNB1008"
_cc=[]

def send_mail(sub,content,tolist):
    #msg = MIMEText(content,_charset="utf-8")
    msg = MIMEText(content,'html','utf-8')
    msg['Subject'] = sub
    msg['From'] = _user
    msg['To'] = ";".join(tolist)
    msg['Cc'] = ";".join(_cc)
    emails = _to + _cc
    try:
        server = smtplib.SMTP()
        server.connect(_host)
        server.login(_user,_pass)
        #server.sendmail(_user,_to,msg.as_string())
        server.sendmail(_user,emails,msg.as_string())
        server.close()
        return True
    except Exception as e:
        print(str(e))
        return False

    
if __name__ == '__main__':
    if send_mail("hello","hello world!"):
        print("Send Successed !")
    else:
        print("Send Failed !")