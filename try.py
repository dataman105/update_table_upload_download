import pymysql
import zipfile
import os

filename1='201801'
olddirectory = 'File0Save/'+filename1
if not os.path.exists('File1Save/'):
    os.makedirs('File1Save/')
newFile= 'File1Save/'+filename1+'.rar'
zip = zipfile.ZipFile(newFile,"w",zipfile.ZIP_DEFLATED)
for path,dirnames,filenames in os.walk(olddirectory):
    # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
    fpath = path.replace(olddirectory,'')
    print(fpath)

    for filename in filenames:
        zip.write(os.path.join(path,filename),os.path.join(fpath,filename))
zip.close()
