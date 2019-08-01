'''邮件通知'''
# from smtplib import SMTP_SSL
import smtplib
from email.mime.text import MIMEText
from email.header import Header

CONFIG={
    "host":"smtp.qq.com",
    "encoding":"utf-8",
    'username':"58296672@qq.com",
    'password':'caiqzvztrbmwbijg',
    'from':"58296672@qq.com"
}

def send_email(to_email:str,text):
    if type(to_email) is str:
        to_email=[to_email]
    smtp = smtplib.SMTP_SSL(CONFIG['host'])
    smtp.set_debuglevel(1)
    smtp.ehlo(CONFIG['host'])
    try:
        smtp.login(CONFIG['username'],CONFIG['password'])
    except:
        raise Exception("邮件认证失败","auth")
    msg = MIMEText(text, "html", CONFIG['encoding'])
    msg['to']=",".join(to_email)
    msg['from']=CONFIG['from']
    msg["Subject"] = Header("Stock Notice", CONFIG['encoding'])
    smtp.sendmail(CONFIG['from'], to_email, msg.as_string())
    smtp.quit()
    return True

    


# if __name__=="__main__":
    # send_email("58296672@qq.com")