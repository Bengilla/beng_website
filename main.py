from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from email.mime.text import MIMEText
import base64
import datetime as dt
import smtplib
import codecs
import os

YEAR = dt.date.today().year

# MY_EMAIL = os.environ['MY_EMAIL']
# MY_PASS = os.environ['MY_PASS']
# R_EMAIL = os.environ['R_EMAIL']
# DATABASE_KEY = os.environ['DATABASE_KEY']
TEST = os.environ['TEST']

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///perform.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config['SECRET_KEY'] = DATABASE_KEY
Bootstrap(app)
db = SQLAlchemy(app)

class UploadData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(300), nullable=False, unique=True)
    director = db.Column(db.String(300), nullable=False)
    light_design = db.Column(db.String(300), nullable=False)
    img_name1 = db.Column(db.String(128), nullable=False)
    img_data1 = db.Column(db.LargeBinary, nullable=False)
    img_render1 = db.Column(db.Text)
    img_name2 = db.Column(db.String(128), nullable=False)
    img_data2 = db.Column(db.LargeBinary, nullable=False)
    img_render2 = db.Column(db.Text)
    img_name3 = db.Column(db.String(128), nullable=False)
    img_data3 = db.Column(db.LargeBinary, nullable=False)
    img_render3 = db.Column(db.Text)
    img_name4 = db.Column(db.String(128), nullable=False)
    img_data4 = db.Column(db.LargeBinary, nullable=False)
    img_render4 = db.Column(db.Text)
    img_name5 = db.Column(db.String(128), nullable=False)
    img_data5 = db.Column(db.LargeBinary, nullable=False)
    img_render5 = db.Column(db.Text)
    
# db.create_all()

def render_picture(data):
    render_pic = base64.b64encode(data).decode('ascii')
    return render_pic

@app.route("/")
def index():
    test = TEST
    program = UploadData.query.order_by(UploadData.year.desc())
    with codecs.open('static/bio/cn_bio.txt', encoding='utf-8') as cn:
        cn_bio = cn.read().splitlines()
    with codecs.open('static/bio/en_bio.txt', encoding='utf-8') as en:
        en_bio = en.read().splitlines()
    return render_template("index.html", year=YEAR, program=program, cn_bio=cn_bio[0], en_bio=en_bio[0], test=test)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        get_year = request.form['year']
        get_title = request.form['title']
        get_director = request.form['director']
        get_lightdesigner = request.form['light_designer']
       
        get_img1 = request.files['image-1']
        get_data_img1 = get_img1.read()
        get_render_img1 = render_picture(get_data_img1)
        get_img2 = request.files['image-2']
        get_data_img2 = get_img2.read()
        get_render_img2 = render_picture(get_data_img2)
        get_img3 = request.files['image-3']
        get_data_img3 = get_img3.read()
        get_render_img3 = render_picture(get_data_img3)
        get_img4 = request.files['image-4']
        get_data_img4 = get_img4.read()
        get_render_img4 = render_picture(get_data_img4)
        get_img5 = request.files['image-5']
        get_data_img5 = get_img5.read()
        get_render_img5 = render_picture(get_data_img5)
        
        save_data = UploadData(
            year=get_year, title=get_title, director=get_director, light_design=get_lightdesigner,
            img_name1=get_img1.filename, img_data1=get_data_img1, img_render1=get_render_img1,
            img_name2=get_img2.filename, img_data2=get_data_img2, img_render2=get_render_img2,
            img_name3=get_img3.filename, img_data3=get_data_img3, img_render3=get_render_img3,
            img_name4=get_img4.filename, img_data4=get_data_img4, img_render4=get_render_img4,
            img_name5=get_img5.filename, img_data5=get_data_img5, img_render5=get_render_img5,
            )
        db.session.add(save_data)
        db.session.commit()
    return render_template("upload.html") 

@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        get_name = request.form["name"]
        get_content = request.form["content"]
        message_body = f"Name: {get_name}<br> Content: {get_content}"
        message = MIMEText(message_body, "html")
        message["Subject"] = f"Subjet: Email from {get_name}"
        message["To"] = R_EMAIL
        message["From"] = MY_EMAIL
        with smtplib.SMTP("smtp.qq.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASS)
            connection.send_message(message)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
