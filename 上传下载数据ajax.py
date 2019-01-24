from flask import Flask,request,jsonify,make_response
import os
import json

app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def upload():
    if request.method=='POST':
        files = request.files.getlist("file2")
        filename=request.form['usr']
        print(filename)
        if not os.path.exists('File0Save/'+str(filename)):
             os.makedirs('File0Save/'+str(filename))
        basePath='File0Save/'+str(filename)
        for file in files:
            file_name = file.filename
            filePath=os.path.join(basePath, file_name)
            file.save(filePath)
    res = make_response(jsonify(basePath))
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'POST'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return res


@app.route('/dld/',methods=['GET','POST'])
def DownLoad():
    mydata=request.get_data().decode('utf-8')
    data = json.loads(mydata)
    res = make_response(jsonify(data))
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'POST'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return res


if __name__ == '__main__':
    app.run('127.0.0.1',8080)