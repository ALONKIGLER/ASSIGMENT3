from flask import request, session, jsonify
import os
from flask import Flask, redirect
from flask import url_for
from flask import render_template
from flask import request
from flask import session
from datetime import timedelta

app = Flask(__name__)

app.secret_key = '123'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=20)

@app.route('/')
def index_func():
    return render_template('home_page.html')


@app.route('/contact')
def contact_func():
    return render_template('contact.html')


@app.route('/about')
def about_page():
    user_info = {'name': 'Alon Kigler', 'number of product': '3', 'product name': 'kiteAlon'}
    session['CHECK'] = 'about'
    return render_template('about_page.html',
                           user_info=user_info)
# -----------------------------------------------------------------------------------
user_dict = {
    'alon': '4444',
    'kigler': '1111',
    'erez': '1111',
    'avu': '1111',
    'haha': '1111'
}

@app.route('/log_in', methods=['GET', 'POST'])
def login_func():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in user_dict:
            pas_in_dict = user_dict[username]
            if pas_in_dict == password:
                session['username'] = username
                session['logedin'] = True
                return render_template('home_page.html',
                                       message='Success',
                                       username=username)
            else:
                return render_template('log_in.html',
                                       message='Wrong password!')
        else:
            return render_template('log_in.html',
                                   message='The user dose not exist')
    return render_template('log_in.html')


@app.route('/log_out')
def logout_func():
    session['logedin'] = False
    session.clear()
    return redirect(url_for('login_func'))



@app.route('/session')
def session_func():
    # print(session['CHECK'])
    return jsonify(dict(session))

# -----------------------------------------------------------------------------------
#
# class Parent:
#     def __init__(self, txt):
#         self.text = txt
#
#
# class Child(Parent):
#     def __init__(self, txt):
#         super().__init__(txt)
#
#     def printmessage(self):
#         print(self.text)
#
#
# x = Child("Hello, and welcome!")
#
# x.printmessage()


users=[{'name': 'kiteAlon', 'size': 'xl', 'price': '1500$', 'img': '1.jpg'},
       {'name': 'kiteErez', 'size': ' l', 'price': '400$', 'img': '2.jpg'},
       {'name': 'kiteDron', 'size': ' xs', 'price': '500$', 'img': '3.jpg'},
       {'name': 'kiteAVI', 'size': ' m', 'price': '700$', 'img': '4.jpg'},
       {'name': 'kiteAlone', 'size': ' s', 'price': '900$', 'img': '1.jpg'} ]

picFolder = os.path.join('static', 'pics')
print(picFolder)
app.config['UPLOAD_FOLDER'] = picFolder


@app.route('/catalog')
def catalog_func():
    if 'user_name' in request.args:
        user_name = request.args['user_name']
        user = next((item for item in users if item['name'] == user_name), None)
        if request.args['user_name'] == "":
            return render_template('catalog_page.html',
                                   users=users)
        if user in users:
            return render_template('catalog_page.html',
                                   user_name=user_name,
                                   pic1_name=os.path.join(app.config['UPLOAD_FOLDER'], user['img']),
                                   user=user)
        else:
            return render_template('catalog_page.html', message='product not found, Please try again ')
    return render_template('catalog_page.html')



if __name__ == '__main__':
    app.run(debug=True)

