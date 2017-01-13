#!/usr/bin/python
#coding: utf-8

import fileinput,os,time,smtplib
from email.mime.text import MIMEText
from email.header import Header

file = 'logs/mover.log'  # 监控的文件名
log = 'monitor_log.log'     # 日志文件名
sleep_time = 20       # 每次读取文件的间隔时间，以秒为单位
recive = ['824363345@qq.com', ]

# 些函数返回两个数，第一个用来表示被监控文件的状态，第二个表示文件的大小
file_size = 0   # 初始文件大小
def get_file_status(file=file):
    '''
    返回 1 表示文件已经刷新了文件名
    返回 2 表示文件没有新增内容
    返回 3 表示文件有新内容
    '''
    try:
        new_size = os.path.getsize(file)
    except OSError:
        with open(log,'a') as f:
            f.write('file not found\n')
    if file_size == 0:
        return 1, new_size
    elif new_size < file_size:
        return 1,new_size
    elif new_size == file_size:
        return 2,new_size
    elif new_size > file_size:
        return 3,new_size


# 匹配错误日志
def find_err_log(text):
    data = text.split(' ')
    try:
        if data[2] == 'ERROR' and int(data[-4][1:-2]) > 20058573 and int(data[-4][1:-2]) < 29158573 and data[
            -6] == 'Duplicate':
            return int(data[-4][1:-2]) - 20000000
        else:
            return 1
    except:
        pass


# 发送邮件的函数，第一个参数是收件人，第二个参数是发送的ID
def sendmail(recive, body):
    sender = 'monitor@reg.qianlima.com'
    recive = recive
    message = MIMEText('重复数据的ID: ' + str(body) + '\n' + '请处理！～～','plain','utf-8')
    message['From'] = Header('千里马强制发布监控系统','utf-8')
    message['To'] = Header('信息部强制发布接收同事','utf-8')
    message['subject'] = Header('强制发布出现未发布数据', 'utf-8')
    try:
        smtpobj = smtplib.SMTP(host='192.168.1.116', port=25)
        smtpobj.sendmail(sender, recive, message.as_string())
        with open(log, 'a') as f:
            f.write(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + ' ' + str(recive) + ' ' + str(body) + '\n')
        print '发送邮件成功'
    except smtplib.SMTPException:
        with open(log, 'a') as f:
            f.write(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + ' 邮件发送失败～' + str(recive) + ' ' + str(body) + '\n')
        print '发送邮件失败'


if __name__ == "__main__":
    while True:
        status,file_size = get_file_status(file)
        if status == 1:                           # 文件刷新了文件名，或第一次运行程序进入
            count = 0
            for i in fileinput.input(file):
                count += 1
                id = find_err_log(i)
                if id > 1:
                    for mail in recive:
                        sendmail(mail,id)
                #print '1'
        elif status == 2:                         # 文件内容一直没有变进入
            #print "文件没有变化"
            pass
        elif status ==3:                          # 文件更新内容进入
            line_num = count
            for i in fileinput.input(file):
                if line_num >= 1:                 # 把已经查看过的行过滤掉
                    line_num -= 1
                    continue
                if line_num < 1:
                    count += 1
                    id = find_err_log(i)
                    if id > 1:
                        for mail in recive:
                            sendmail(mail, id)
                #print '3'
        try:
            time.sleep(sleep_time)
        except KeyboardInterrupt:
            exit()
