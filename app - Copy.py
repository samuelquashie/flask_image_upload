from flask import Flask,render_template,url_for,request,Response
import sqlite3
from form import *
from werkzeug.utils import secure_filename
from uuid import uuid4
import cv2
import os

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png','jpg','jpeg','gif'}
conn = sqlite3.connect('mydata.db',timeout=30,check_same_thread=False)
cursor = conn.cursor()

app = Flask(__name__, static_folder = "static")

app.config['SECRET_KEY'] = 'mySecret_5ecAb[u[K64)'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create table
cursor.execute('''
                CREATE TABLE IF NOT EXISTS upload
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    lname TEXT,
                    fname TEXT,
                    img TEXT,
                    name TEXT,
                    mimetype TEXT
                )
        ''')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

# Convert image to grayscale
def rgb_to_gray(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    return gray

@app.route('/',methods=['POST','GET'])
def index():
    form = ImageFile()
    if request.method == 'POST':
        file = request.files['file']
        # file = form.image.data
        lname = form.lname.data
        fname = form.fname.data
        # print(file)
        if file.filename == '':
            return 'No file selected!'
            # return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)+fname+'_'+lname+'.jpg'
            name = filename
            img = file.read()
            mimetype = file.mimetype
            # Saves image in database
            cursor.execute('INSERT INTO upload(lname,fname,img,name,mimetype) VALUES (?,?,?,?,?)',(lname,fname,img,name,mimetype))
            conn.commit()
            # Uploads image to image folder
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'File uploaded.'

        file = request.files['file']
    return render_template('index.html',form=form)

@app.route('/<int:id>')
def get_img(id):
    cursor.execute('SELECT * FROM upload WHERE id=?',(id,))
    res = cursor.fetchone()
    if not res:
        return 'Image not found!'
    return Response(res[1],mimetype=res[3])

if __name__ == '__main__':
    app.run(debug=True)