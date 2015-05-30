#!flask/bin/python

#imports
import sqlite3
from flask import Flask, request, g, render_template

#config
DATABASE = "gallery.db"


#creating flask app instance
app = Flask(__name__)
app.config.from_object(__name__)

#connection with db
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/', methods = ['GET', 'POST'])
def paint():
    if request.method == 'GET':
        return render_template('my_paint.html')
            
    else:   # if request.method == 'POST'
        filename = request.form['filename']
        imgdata = request.form['imgdata']
        g.db.execute('INSERT INTO gallery(filename, filedata) VALUES(?, ?)', (filename, imgdata))
        g.db.commit()

@app.route('/gallery', methods = ['GET', 'POST'])
@app.route('/gallery/<imagename>', methods = ['GET', 'POST'])
def gallery(imagename = None):
    cur = g.db.execute('SELECT filename FROM gallery')
    pics = [row[0] for row in cur.fetchall()]

    if request.method == 'GET':
        if not imagename:
            g.db.close()
            return render_template('gallery.html', pics = pics)

        else:
            curimg = g.db.execute('SELECT filedata FROM gallery WHERE filename=?', (imagename,))
            data = curimg.fetchone()[0]
            g.db.close()
            return render_template('gallery.html', img = data, pics = pics)

if __name__ == '__main__':
    app.run(debug = True)
