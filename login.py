#!/usr/bin/env python
#coding:utf-8
__author__ = 'anbaoyong'
import json
import os,sys
import time
import commands
from flask import url_for,Flask,request,render_template,redirect,make_response,session
app = Flask(__name__)

HOST = '0.0.0.0'
PORT = 8888

def sess_check(func):
    def sess(*args,**kw):
    	if username in session:
            return  func(*args,**kw)
    	else:
            return redirect('/')
    return sess


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login',methods=['GET','POST'])
def login():
    global username
    if request.method == 'POST':
        username = request.form.get('username')
        passwd = request.form.get('passwd')
        if username == "admin" and  passwd == "admin#%^&*":
            session[username] = username
            return redirect('/add_dns')

        else:
            return redirect('/')
    return redirect('/')

@app.route('/add_dns')
@sess_check
def add_dns():
    return render_template('dns.html')

@app.route('/sub',methods=['GET','POST'])
def sub():
    fqdn = []
    stime = time.strftime('%Y%m%d_%H%M',time.localtime())
    file = '/root/dn/domain_%s.txt' % stime 
    if request.method == 'POST':
        ip = request.form.get('ips')
	if not ip.strip():
	    return '输入不能为空'
        fqdn = ip.split('\r\n')
        with open(file,'w') as f:
            for i in fqdn:
		if i.strip():
                    f.write('%s\n' % i)
	if os.path.exists(file):
	    #status = os.system('ddnstool -a %s' % file)
	    (status, output) = commands.getstatusoutput('ddnstool -a %s' % file)
	    if not status:
		return 'success: %s' % output
	    else:
		return 'fail: %s' % output
        else:
	    return 'file not exists'
        
       # username = request.form.get('username')
       # passwd = request.form.get('passwd')
       # if username == "admin" and  passwd == "admin":
       #     session['username'] = username
       #     return redirect(url_for('ip.html'))

       # else:
       #     return redirect('/')
    return redirect('/add_dns')

#@app.route('/logout')
#def logout():
#    session.pop('username', None)
#    return redirect('/')




if __name__ == '__main__':
    username = ''
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(host=HOST,port=PORT,debug=True)
