from flask import Flask, render_template, request, redirect, session
import mysql.connector

# Konfigurasi aplikasi Flask
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Konfigurasi MySQL
from config import DB_CONFIG
db_connection = mysql.connector.connect(**DB_CONFIG)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        
        if user:
            session['user_id'] = user['id']
            return redirect('/dashboard')
        else:
            return "Login gagal! Coba lagi.", 401

    return render_template('login.html')


# Logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')


# Halaman Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM data_donat")
    data = cursor.fetchall()
    cursor.close()
    return render_template('dashboard.html', data=data)


# Tambah Data
@app.route('/add', methods=['POST'])
def add():
    if 'user_id' not in session:
        return redirect('/login')
    
    category = request.form['category']
    value = request.form['value']
    
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO data_donat (category, value) VALUES (%s, %s)", (category, value))
    db_connection.commit()
    cursor.close()
    return redirect('/dashboard')


# Edit Data
@app.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    if 'user_id' not in session:
        return redirect('/login')
    
    category = request.form['category']
    value = request.form['value']
    
    cursor = db_connection.cursor()
    cursor.execute("UPDATE data_donat SET category = %s, value = %s WHERE id = %s", (category, value, id))
    db_connection.commit()
    cursor.close()
    return redirect('/dashboard')


# Hapus Data
@app.route('/delete/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect('/login')
    
    cursor = db_connection.cursor()
    cursor.execute("DELETE FROM data_donat WHERE id = %s", (id,))
    db_connection.commit()
    cursor.close()
    return redirect('/dashboard')


if __name__ == '__main__':
    app.run(debug=True)
