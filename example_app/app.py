from flask import Flask, render_template, request, redirect, url_for
import cv2
import numpy as np
import math
import csv
import sys
import os

sys.path.insert(1, './src')
import main


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    s = ""
    name = ""
    if request.method == 'POST':
        req = request.form

        name = req.get("name")
        print(f"Namn: {name}")

        f = request.files['file']
        f.save(f.filename)
        
        image_path = f.filename

        c = main.process(image_path)
    
        
        os.rename("./out/4correct.jpg", f"./example_app/static/{image_path}.jpg")
        image = f"/static/{image_path}.jpg"


    return render_template('response.html', res=c, namn=name, image=image)

@app.route('/confirm', methods = ['GET', 'POST'])
def confirm():
    name = ""
    r = ""
    d = ""
    if request.method == 'POST':
        req = request.form

        name = req.get("name")
        print("Namn: " + name)

        r = req.get("corr")
        print("rätt: " + name)

        d = req.get("decQue")
        print("d: " + name)

        with open("./example_app/templates/results.csv", 'a') as f:
            writer = csv.writer(f)
            writer.writerow([name, r, d])

    return redirect(url_for('res'))

@app.route('/man', methods = ['GET', 'POST'])
def man():
    name = ""
    r = ""
    d = ""
    if request.method == 'POST':
        req = request.form

        name = req.get("name")
        print("Namn: " + name)

        r = req.get("corr")
        print("rätt: " + name)

        d = req.get("decQue")
        print("d: " + name)

        with open("./example_app/templates/results.csv", 'a') as f:
            writer = csv.writer(f)
            writer.writerow([name, r, d])

    return render_template("manuell.html")


@app.route('/results')
def res():
    results = []
    with open('./example_app/templates/results.csv') as csv_file:
        lines = csv.reader(csv_file, delimiter=',')
        line_count = 0

        for row in lines:
            if len(row) != 0:
                results.append(row)
        
        print(results)

    return render_template('results.html', results=results)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')