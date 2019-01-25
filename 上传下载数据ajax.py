from flask import Flask,request,jsonify,make_response
import os
import json
import pymysql
import zipfile


dbip='172.16.1.206'
dbusr='chenyoulin'
dbpwd='chenyoulin'
dbname='spider'

app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def upload():
    if request.method=='POST':
        files = request.files.getlist("file2")
        filename=request.form['usr']
        if not os.path.exists('File0Save/'+str(filename)):
             os.makedirs('File0Save/'+str(filename))
        basePath='File0Save/'+str(filename)
        for file in files:
            file_name = file.filename
            filePath=os.path.join(basePath, file_name)
            file.save(filePath)
    res = make_response(jsonify(basePath+'/'+file_name))
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'POST'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return res


@app.route('/down/',methods=['GET','POST'])
def DownLoad():
    if request.method == 'POST':
        filename1 = request.form['mydata']
        print(filename1)
    olddirectory = 'File0Save/' + filename1
    if not os.path.exists('File1Save/'):
        os.makedirs('File1Save/')
    newFile = 'File1Save/' + filename1 + '.rar'
    zip = zipfile.ZipFile(newFile, "w", zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(olddirectory):
        # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
        fpath = path.replace(olddirectory, '')
        for filename in filenames:
            zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
    zip.close()
    res = make_response(newFile)
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'POST'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return res

@app.route('/table/',methods=['GET','POST'])
def showData():
    conn = pymysql.connect(dbip,dbusr,dbpwd,dbname, charset='utf8')
    cur = conn.cursor()
    sel = 'select * from tab_myself_data_2019;'
    cur.execute(sel)
    xy = cur.fetchall()
    mydata=[]
    for z in xy:
        bh, xm, zw, usrname = z
        mydata.append({'bh':bh,  'xm': xm, 'zw':zw})
    cur.close()
    conn.close()
    res = make_response(jsonify(mydata))
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'POST'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return res

@app.route('/dele/',methods=['GET','POST'])
def deldata():
    usrname = request.form['usrname']
    bh=request.form['bh']
    print(bh)
    # xm=request.form['xm']
    # zw=request.form['zw']
    conn = pymysql.connect(dbip,dbusr,dbpwd,dbname, charset='utf8')
    cur = conn.cursor()
    sel = 'delete from tab_myself_data_2019 where bh=%s and usrname=%s;'
    cur.execute(sel,(bh,usrname))
    conn.commit()
    cur.close()
    conn.close()
    res=make_response(jsonify('删除成功'))
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'POST'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return res

@app.route('/insert/',methods=['GET','POST'])
def insertData():
    mydata = request.get_data().decode('utf-8')
    mydata=json.loads(mydata)
    usrname = mydata['usrname']
    bh=mydata['bh']
    xm=mydata['xm']
    zw=mydata['zw']
    conn = pymysql.connect(dbip,dbusr,dbpwd,dbname, charset='utf8')
    cur = conn.cursor()
    sel = 'insert into tab_myself_data_2019 set bh=%s,xm=%s,zw=%s,usrname=%s;'
    cur.execute(sel,(bh,xm,zw,usrname))
    conn.commit()
    cur.close()
    conn.close()
    print(usrname)
    res=make_response(jsonify('插入成功'))
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'POST'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return res


@app.route('/update/',methods=['GET','POST'])
def updateData():
    mydata = request.get_data().decode('utf-8')
    mydata=json.loads(mydata)
    usrname = mydata['usrname']
    bh=mydata['td1']
    xm=mydata['td2']
    zw=mydata['td3']
    conn = pymysql.connect(dbip,dbusr,dbpwd,dbname, charset='utf8')
    cur = conn.cursor()
    sel = 'update tab_myself_data_2019 set bh=%s,xm=%s,zw=%s,usrname=%s where bh=%s and usrname=%s;'
    cur.execute(sel,(bh,xm,zw,usrname,bh,usrname))
    conn.commit()
    cur.close()
    conn.close()
    print(mydata)
    res=make_response(jsonify('插入成功'))
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'POST'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return res

if __name__ == '__main__':
    app.run('127.0.0.1',8089)