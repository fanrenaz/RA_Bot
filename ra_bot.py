# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 22:52:33 2020

@author: Yifan Ren
"""

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import time

def send_email(my_receiver, subject, body):
    ret=True
    try:
        my_sender = 'renyifan@yifan-ren.com'
        password = 'WLrng5A4gHGyCWcD' # Invalid, just for example
        smtp_server = 'smtp.exmail.qq.com' #ServerAdd
        msg=MIMEText(body,'plain','utf-8')#Body Content
        msg['From']=formataddr(["xx",my_sender])#From
        msg['To']=formataddr(["xx",my_receiver])#To        
        msg['Subject']=subject #Subject
        server = smtplib.SMTP_SSL(smtp_server, 465)
        server.login(my_sender, password)
        server.sendmail(my_sender, [my_receiver], msg.as_string()) 
        server.quit()
    except Exception:  
        ret=False
    return ret

def scrape(first_time = False):
    ourUrl=urllib.request.urlopen("https://www.nber.org/jobs/nonnberjobs.html")
    soup=BeautifulSoup(ourUrl,'lxml')
    results = []
    for p in soup.find_all("p"):
        each = p.text.split("\n")[:4]
        link = p.a['href']
        if link.startswith("http") is False:
            link = "https://www.nber.org/jobs/"+link
        each.append("Application Link: "+link)
        results.append(each)
    df = pd.DataFrame(results[1:-5])
    if first_time == True:
        return df.to_csv("./data/historical_total.csv",sep=";",index=False,header=False)
    else:return df.to_csv("./data/recent_total.csv",sep=";",index=False,header=False)

 def check_update():
    with open("./data/historical_total.csv") as old:
        line_old = old.readline().split(";")
    update = []
    with open("./data/recent_total.csv") as new:
        #line_new = new.readline().split(";")
        n = 0
        while True:
            line_new = new.readline().split(";")
            if line_new == line_old: 
                break
            else:
                update.append(line_new)
                n += 1
    if n !=0: 
        print("New positions found")
        return n, update
    else: return None
    
def construct_mail():
    content = """New Positions Updated! \n
                 \n"""   
    for i in range(len(update)):
        content = content+"The No.{} position updated.".format(i+1)+"\n"+"\n".join(update[i])+"\n"
    return content
    
def main():
    im = False
    while im == False:
        im = send_email(my_receiver, subject, body)
        time.sleep(2)
