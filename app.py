
from flask import Flask, flash, redirect, render_template, request, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from werkzeug.security import generate_password_hash, check_password_hash

import secrets
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from werkzeug.utils import secure_filename
import os


def  generar_token (email):
    token = secrets.token_urlsafe(32)
    expiry=  datetime.now () + timedelta(hours =1)
    cur = mysql.connection.cursor()
    cur.execute("UPDATE usuarios SET reset_token= %s, token_expiry= %s WHERE username = %s", (token, expiry, email))
    mysql.connection.commit()
    cur.close()
    return token
def enviar_correo_reset(email,token):
    enlace = url_for('reset', token = token, _external=True)
    cuerpo = f"""Hola, solicitaste recuperar tu contraseña. Haz click en el siguiente enlace:
    {enlace}
    Este enlace expirará en 1 hora.
    Si no lo solicitó, ignore este mensaje. """

    remitente = 'jeonmagalum@gmail.com'
    clave = 'twwg oxei qcrg inyd'
    mensaje = MIMEText(cuerpo)
    mensaje['Subject'] = 'Recuperar contraseña'
    mensaje['From'] = 'jeonmagalum@gmail.com'
    mensaje['To'] = email

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(remitente,clave)
    server.sendmail(remitente,email,mensaje.as_string())
    server.quit()

app = Flask(__name__)
app.config["MYSQL_HOST"]= "localhost" #servidor xampp
app.config["MYSQL_USER"]= "root" # usuario 
app.config["MYSQL_PASSWORD"]= ""
app.config["MYSQL_DB"]= "paw_pet"  # nombre de la base

mysql = MySQL(app)
app.secret_key = 'Maya'
@app.route("/")
def index():
    #usuamos render_template para mostar el archivo 'index,html'
 return render_template ('index.html')

@app.route('/login', methods =['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'] #se almacena en esta variable 
        password_ingresada = request.form['password'] 
        
        cur = mysql.connection.cursor()#metodo cursor
        cur.execute("SELECT u.idUsuario,u.nombre,u.password,r.nombreRol FROM usuarios u JOIN usuario_rol ur ON u.idUsuario=ur.idUsuario JOIN roles r ON ur.idRol=r.idRol WHERE u.username = %s",(username,))
        usuario = cur.fetchone()
        cur.close # va a cerrar esta conexion ( es el objeto de conexio de una base de datos)
        
        if usuario and check_password_hash (usuario[2], password_ingresada):
            session ['usuario'] = usuario[1]
            session['rol'] = usuario [3]
            flash(f"¡Bienvenido {usuario [1]}!")

            if usuario[3]=='Admin':
                return redirect(url_for('dashboard'))
            elif usuario[3]== 'Usuario':
                return redirect(url_for('index'))
            else: 
                flash("rol no reconocido")
                return redirect(url_for('login'))
        else:
            flash("usuario o contraseña incorrecta")
    return render_template('login.html')
 
@app.route ('/logout')
def logout():
     session.clear()
     flash("sesion cerrada correctamente")
     return redirect(url_for('login'))
 
 
 

@app.route('/registrarse', methods=['GET','POST'])
def registrarse():
    if request.method == 'POST':
        nombre = request.form ['nombre']
        apellido = request.form ['apellido']
        username = request.form ['username']
        password = request.form ['password']
        hash = generate_password_hash (password)
        cur = mysql.connection.cursor()
        try:
            cur.execute("""INSERT INTO usuarios(nombre,apellido,username,password) VALUES (%s,%s,%s,%s)
                      """, (nombre, apellido, username, hash))
            mysql.connection.commit()

            cur.execute("SELECT idUsuario FROM usuarios WHERE username=%s",(username,))
            nuevoUsuario=cur.fetchone()
            cur.execute("INSERT INTO usuario_rol(idUsuario,idRol) VALUES (%s,%s)",(nuevoUsuario[0],2))
            mysql.connection.commit()

            flash('Usuario registrado con éxito')
            return redirect(url_for('login'))
        except:
            flash('Este correo ya está registrado')
        finally:
            cur.close()
    return render_template('registrarse.html')

@app.route('/recuperar_contraseña',methods=['GET','POST'])
def recuperar_contraseña():
    if request.method =='POST':
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("SELECT idUsuario FROM usuarios WHERE username = %s", (email,))
        existe = cur.fetchone()
        cur.close()

        if not existe:
          flash("Este correo no está registrado.")
          return redirect(url_for('recuperar_contraseña'))   
     
        token = generar_token(email)
        enviar_correo_reset(email,token)

        flash("Se le envío un correo con el enlace para restablecer su contraseña")
        return redirect(url_for('login'))
    return render_template('recuperar_contraseña.html')
    
    #Ruta recuperar contraseña
@app.route('/reset/<token>', methods = ['GET','POST'])
def reset (token):
    cur =mysql.connection.cursor()
    cur.execute("SELECT idUsuario, token_expiry FROM usuarios WHERE reset_token = %s", (token,))
    usuario = cur.fetchone()
    cur.close()

    if not usuario or datetime.now() >usuario [1]:
        flash ("token inválido o expirado.")
        return redirect(url_for('recuperar_contraseña'))
    
    if request.method =='POST':
        nuevo_password = request.form['password']
        hash_nueva = generate_password_hash(nuevo_password)
        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE usuarios SET password=%s, reset_token=NULL, token_expiry=NULL WHERE idUsuario=%s", (hash_nueva, usuario[0]))
        mysql.connection.commit()
        cur.close()

        flash ("Su contraseña ha sido actualizada.")
        return redirect(url_for('login')) 

    return render_template('reset.html')

def inventario():
    #if 'rol' not in session or session['rol'] != 'admin':
    #    flash("acceso  restringido solo parfa los administradores")
    #    return redirect(url_for('login'))
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    cursor.close()
    return render_template('inventario.html', productos=productos)

@app.route('/inventario')
def inventario():
    #if 'rol' not in session or session['rol'] != 'admin':
    #    flash("acceso  restringido solo parfa los administradores")
    #    return redirect(url_for('login'))
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    cursor.close()
    return render_template('inventario.html', productos=productos)

@app.route('/agregar_producto', methods=['GET','POST'])
def agregar_producto():
    #if 'rol' not in session or session['rol'] != 'admin':
    #   flash("acceso  restringido solo parfa los administradores")
    #    return redirect(url_for('login'))
    if request.method=='POST':
        nombre=request.form['nombre']
        descripcion=request.form['descripcion']
        precio=request.form['precio']
        imagen=request.files['imagen']
        cantidad=request.form['cantidad']

        
        filename=secure_filename(imagen.filename)
        imagen.save(os.path.join('static/uploads',filename))
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO productos (nombre_producto,descripcion,precio,cantidad,imagen)VALUES(%s,%s,%s,%s,%s)",(nombre,descripcion,precio,cantidad,filename))
        mysql.connection.commit()
        cursor.close()

        flash("producto almacenado correctamente")
        return redirect(url_for('inventario'))
    return render_template('agregar_producto.html')

        
        

@app.route('/sobre_nosotras')
def sobre_nosotras ():
    return render_template('sobre_nosotras.html')

@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        flash("Debes iniciar sesion para acceder al dasboard")
        return redirect(url_for('login'))
    cursor = mysql.connect.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT idUsuario,nombre, apellido,username FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    return render_template('dashboard.html', usuarios=usuarios)


@app.route('/eliminar/<int:id>')
def eliminar(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM usuarios WHERE idUsuario=%s' ,(id,))
    mysql.connection.commit()
    cursor.close()
    flash ('Usuario eliminado')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(port=5000, debug=True)
    

