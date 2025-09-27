
from flask import Flask, flash, redirect, render_template, request, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["MYSQL_HOST"]= "localhost" #servidor xampp
app.config["MYSQL_USER"]= "root" # usuario 
app.config["MYSQL_PASSWORD"]= ""
app.config["MYSQL_DB"]= "paw_pet"  # nombre de la base

mysql = MySQL(app)
app.secret_key = 'tu_clave_secreta_super_segura'
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
        cur.execute("SELECT idUsuario, nombre, password FROM usuarios WHERE username = %s",(username,))
        usuario = cur.fetchone()
        cur.close # va a cerrar esta conexion ( es el objeto de conexio de una base de datos)
        
        if usuario and check_password_hash (usuario[2], password_ingresada):
            session ['usuario'] = usuario[1]
            flash(f"¡Bienvenido {usuario [1]}!")
            return redirect(url_for('dashboard'))
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
            flash('Usuario registrado con éxito')
            return redirect(url_for('login'))
        except:
            flash('Este correo ya está registrado')
        finally:
            cur.close()
    return render_template('registrarse.html')

    


@app.route('/recuperar_contraseña')
def recuperar_contraseña():
    return render_template('recuperar_contraseña.html')

@app.route('/inventario')
def inventario ():
    #if 'rol' not in session or session['rol'] !='admin'
    return render_template('inventario.html')




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

    @app.route('/inventario')
    def inventario():
        if 'rol' not in session or session ['rol'] != 'admin': 
         flash("acceso restringido solo para los administradores")                                  
        return redirect(url_for('login'))
        return render_template('inventario.html')
                        
       

    
       

    

