# -*- encoding:utf-8 -*-

from flask import Flask,request,redirect,render_template,url_for
import modules.file_controll as Fc
import json

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/getPicture',methods=['GET','POST'])
def getPicture():
  if request.method == 'POST':

    if 'faceImg' not in request.files:
      print "no files"
      return redirect('http://localhost:5000/takePicture')

    msg,result = Fc.image_save(request.files['faceImg'])
    if result:
      return render_template('getPicture.html',imgUrl=msg)

    else:
      return redirect('http://localhost:5000/takePicture')

  else:

    return render_template('index.html')

@app.route('/save_json',methods=['POST'])
def save_json():
    json_file = open("image.json","w")
    try:
      json.dump(request.get_json(),json_file)
      return "success"

    except:
      return "failed"

if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0',port=8000)
