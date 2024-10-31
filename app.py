from flask import Flask,render_template,url_for,request,Response
import sqlite3
from form import *
from werkzeug.utils import secure_filename
import uuid

ALLOWED_EXTENSIONS = {'png','jpg','jpeg','gif'}
conn = sqlite3.connect('mydata.db',timeout=30,check_same_thread=False)
cursor = conn.cursor()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mySecret_5ecAb[u[K64)'

# Create table
cursor.execute('''
                CREATE TABLE IF NOT EXISTS upload
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    img TEXT,
                    name TEXT,
                    mimetype TEXT
                )
        ''')

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/',methods=['POST','GET'])
def index():
    form = ImageFile()
    if request.method == 'POST':
        # file = request.files['file']
        file = form.image.data
        print(file)
        if file.filename == '':
            return 'No file part!'
        if file:
            filename = secure_filename(file.filename)
            name = filename
            img = file.read()
            mimetype = file.mimetype
            cursor.execute('INSERT INTO upload(img,name,mimetype) VALUES (?,?,?)',(img,name,mimetype))
            conn.commit()
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