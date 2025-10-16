
from flask import Flask, flash, redirect, render_template, request, url_for, session,jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
from werkzeug.security import generate_password_hash, check_password_hash

import secrets
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from werkzeug.utils import secure_filename
import os
import requests
import threading
import time

# Configuración de CallMeBot (alertas por WhatsApp)
WHATSAPP_PHONE = "573133874470"  # tu número con código de país, ej: 573001234567
WHATSAPP_API_KEY = "1096550"  # la clave que te dio CallMeBot


def enviar_alerta_whatsapp(mensaje):
    """Envía un mensaje de WhatsApp usando CallMeBot."""
    try:
        url = f"https://api.callmebot.com/whatsapp.php?phone={WHATSAPP_PHONE}&text={mensaje}&apikey={WHATSAPP_API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            print("Mensaje de WhatsApp enviado correctamente")
        else:
            print("Error al enviar mensaje:", response.text)
    except Exception as e:
        print("Error al conectar con CallMeBot:", e)

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

@app.context_processor
def contar_items_carrito():
    if 'idUsuario' in session:
        idUsuario = session ['idUsuario']
        cursor = mysql.connection.cursor()
        cursor.execute("""
                       SELECT SUM(dc.cantidad)
                       FROM detalle_carrito dc
                       JOIN carrito c ON dc.idCarrito = c.idCarrito
                       WHERE c.idUsuario = %s
                       """,(idUsuario,))
        cantidad = cursor.fetchone()[0]
        cursor.close()
        return dict(carrito_cantidad=cantidad if cantidad else 0)
    return dict(carrito_cantidad=0)
     
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
        cur.execute("""
        SELECT u.idUsuario, u.nombre, u.password, r.nombreRol
        FROM usuarios u
        JOIN usuario_rol ur ON u.idUsuario= ur.idUsuario  
        JOIN roles r ON ur.idRol = r.idRol
        WHERE u.username =%s            
        """,(username,))

        usuario = cur.fetchone()
        
        
        if usuario and check_password_hash (usuario[2], password_ingresada):
            session['idUsuario']= usuario[0]
            session ['usuario'] = usuario[1]
            session['rol'] = usuario [3]
            flash(f"¡Bienvenido {usuario [1]}!")

            cur.execute("""
            INSERT INTO registro_login (idUsuario, fecha)
            VALUES (%s, NOW ())
            """, (usuario[0],))
            mysql.connection.commit()

            cur.close()

            if usuario[3]=='Admin':
                return redirect(url_for('dashboard'))
            elif usuario[3]== 'Usuario':
                return redirect(url_for('index'))
            else: 
                flash("Rol no reconocido")
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
    cursor.execute("SELECT idCategoria, nombre FROM categorias") 
    categorias = cursor.fetchall()
    cursor.close()
    
    return render_template('inventario.html', productos=productos, categorias=categorias)




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

        
        



@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        flash("Debes iniciar sesion para acceder al dasboard")
        return redirect(url_for('login'))
    cursor = mysql.connect.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""
      SELECT  u.idUsuario, u.nombre, u.apellido, u.username, r.nombreRol, ur.idRol
      FROM usuarios u
      LEFT JOIN usuario_rol ur ON u.idUsuario = ur.idUsuario
                   LEFT JOIN roles r ON ur.idRol = r.idRol
        """)
    usuarios = cursor.fetchall()
    cursor.close()
    return render_template('dashboard.html', usuarios=usuarios)

#Editar usuario
@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar (id):
    nombre=request.form ['nombre'] 
    apellido=request.form ['apellido'] 
    correo=request.form ['correo'] 
    rol = request.form ['rol']

    cursor = mysql.connection.cursor()
    cursor.execute (""" UPDATE usuarios SET nombre= %s, apellido =%s, username=%s WHERE idUsuario=%s""",(nombre,apellido,correo,id))
    cursor.execute ("SELECT * FROM usuario_rol WHERE id Usuario =%s", (id,))
    existe = cursor.fetchone()

    if existe:
        cursor.execute("UPDATE usuario_rol SET idRol =%s WHERE idUsuario=%s", (rol,id) )
    else:
        cursor.execute("INSERT INTO usuario_rol(idUsuario, idRol) VALUES (%s, %s)", (id,rol))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('dashboard'))


@app.route('/eliminar/<int:id>')
def eliminar(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM usuarios WHERE idUsuario=%s' ,(id,))
    mysql.connection.commit()
    cursor.close()
    flash ('Usuario eliminado')
    return redirect(url_for('dashboard'))

#buscador
@app.route('/buscar')
def buscar():
    try:
        q = request.args.get('q', '').strip()
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        if q:
            cur.execute("""
                SELECT idProducto, nombre_producto, descripcion, precio, cantidad, imagen
                FROM productos
                WHERE nombre_producto LIKE %s OR descripcion LIKE %s
            """, (f"%{q}%", f"%{q}%"))
        else:
            cur.execute("""
                SELECT idProducto, nombre_producto, descripcion, precio, cantidad, imagen
                FROM productos
            """)

        productos = cur.fetchall()
        cur.close()
        return jsonify(productos)
    
    except Exception as e:
        print("❌ Error en /buscar:", e)
        return jsonify({"error": str(e)}), 500


 #catalogo
@app.route ('/catalogo')
def catalogo():
     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute("SELECT * FROM productos")
     productos = cursor.fetchall()
     cursor.close()
     return render_template('catalogo.html', productos=productos)
 
@app.route('/agregarCarrito/<int:id>', methods=['POST'])
def agregarCarrito(id):
    if'usuario' not in session:
        flash("debes iniciar sesión para comprar.")
        return redirect(url_for('login'))
     
    cantidad = int(request.form['cantidad'])
    idUsuario = session.get('idUsuario')
     
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT cantidad FROM productos WHERE idProducto =%s", (id,))
    stock = cursor.fetchone()[0]
    cursor.execute("SELECT idCarrito FROM carrito WHERE idUsuario =%s", (idUsuario,))
    carrito = cursor.fetchone()
     
    if not carrito:
        cursor.execute("INSERT INTO carrito(idUsuario) VALUES (%s)", (idUsuario,))
        mysql.connection.commit()
        cursor.execute("SELECT LAST_INSERT_ID()")
        carrito = cursor.fetchone()
     
    idCarrito = carrito[0]
     
    cursor.execute(""" SELECT cantidad FROM detalle_carrito
                    WHERE idCarrito = %s AND idProducto =%s 
                     """,(idCarrito,id))
    existente = cursor.fetchone()
    cantidad_total = cantidad
   
    if existente:
        cantidad_total += existente[0]
   
    if cantidad_total > stock:  
        flash("no puedes agragar más unidades  de las disponibles","warning")
        cursor.close()
        return redirect(url_for('catalogo'))
         
    if existente:
        nueva_cantidad = existente[0] + cantidad
        cursor.execute("""
                       UPDATE detalle_carrito
                       SET cantidad = %s
                       WHERE idCarrito = %s AND idProducto = %s
                       """, (nueva_cantidad, idCarrito,id))      
    else:
        cursor.execute("""
            INSERT INTO detalle_carrito(idCarrito, idProducto, cantidad)
            VALUES (%s,%s,%s)
            """,(idCarrito, id, cantidad))
         
    mysql.connection.commit()
    cursor.close()
         
    flash("Producto agregado al carrito")
    return redirect(url_for('catalogo'))


@app.route('/carrito')
def carrito():
    if'usuario' not in session:
       flash("debes iniciar sesion para comprar.")
       return redirect(url_for('login'))
     
    idUsuario = session.get('idUsuario')
     
    cursor = mysql.connect.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""
                SELECT p.idProducto, p.nombre_producto, p.precio, p.imagen, dc.cantidad, p.cantidad AS stock
                FROM detalle_carrito dc
                JOIN carrito c ON dc.idCarrito = c.idCarrito
                JOIN productos p ON dc.idProducto = p.idProducto
                WHERE c.idUsuario = %s
                    """, (idUsuario,))
    productos_carrito = cursor.fetchall()
    cursor.close()
    total = sum(item['precio'] * item['cantidad'] for item in productos_carrito)
   
    return render_template('carrito.html', productos=productos_carrito, total = total)

@app.route('/actualizar_carrito/<int:id>', methods=["POST"])
def actualizar_carrito(id):
    accion = request.form.get("accion")
    cantidad_actual = int(request.form.get("cantidad_actual",1))
    idUsuario = session.get("idUsuario")
    
    if accion == "sumar":
        nueva_cantidad = cantidad_actual +1
    elif accion == "restar":
        nueva_cantidad = max(1, cantidad_actual -1)
    else: 
        nueva_cantidad = int(request.form.get("cantidad_manual", cantidad_actual) )

    cursor = mysql.connection.cursor()

    cursor.execute("SELECT cantidad FROM productos WHERE idProducto = %s", (id,))
    stock = cursor.fetchone()[0]

    if nueva_cantidad > stock:
        flash("No puedes exceder el inventario disponible", "warning")
        cursor.close()
        return redirect(url_for("carrito"))
    if nueva_cantidad > 0:
        cursor.execute("""
                UPDATE detalle_carrito dc
                JOIN carrito c ON dc.idCarrito = c.idCarrito
                SET dc.cantidad = %s
                WHERE c.idUsuario = %s AND dc.idProducto = %s 
                """, (nueva_cantidad, idUsuario, id))
    else:
        cursor.execute("""
                DELETE dc FROM detalle_carrito dc
                JOIN carrito c ON dc.idCarrito = c.idCarrito
                WHERE c.idUsuario = %s AND dc.idProducto = %s
                     """,(idUsuario,id))    
    mysql.connection.commit()
    cursor.close()
    
    flash("carrito actualizado", "info")
    return redirect(url_for("carrito")) 
   
@app.route("/eliminar_del_carrito/<int:id>")
def eliminar_del_carrito(id):
    idUsuario = session.get("idUsuario")
    cursor = mysql.connection.cursor()
    cursor.execute("""
                DELETE dc FROM detalle_carrito dc
                JOIN carrito c ON dc.idCarrito = c.idCarrito
                WHERE c.idUsuario = %s AND dc.idProducto = %s
                    """,(idUsuario,id)) 
    mysql.connection.commit()
    cursor.close()
    flash("Producto Eliminado", "danger")
    return redirect(url_for("carrito")) 

@app.route("/vaciar_carrito")
def vaciar_carrito():
    idUsuario = session.get("idUsuario")
    cursor = mysql.connection.cursor()
    cursor.execute("""
                DELETE dc FROM detalle_carrito dc
                JOIN carrito c ON dc.idCarrito = c.idCarrito
                WHERE c.idUsuario = %s  
                    """,(idUsuario,)) 
    mysql.connection.commit()
    cursor.close()
    flash("Carrito Vaciado", "warning")
    return redirect(url_for("carrito")) 
    

#inicio inventario

@app.route('/editar_producto/<int:id>', methods=['POST'])
def editar_producto(id):
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    precio = request.form['precio']
    cantidad = request.form['cantidad']
    imagen = request.files['imagen']
    
    cursor= mysql.connection.cursor()
    if imagen and imagen.filename != '':
        filename = secure_filename(imagen.filename)
        imagen.save(os.path.join('static/uploads', filename))
        cursor.execute("""
                       UPDATE productos
                       SET nombre_producto=%s, descripcion=%s, precio=%s, cantidad=%s, imagen=%s
                       WHERE idProducto=%s
                       """, (nombre, descripcion, precio, cantidad, filename, id))
    else:
        cursor.execute("""
                       UPDATE productos
                       SET nombre_producto=%s, descripcion=%s, precio=%s, cantidad=%s
                       WHERE idProducto=%s
                       """, (nombre, descripcion, precio, cantidad, id))
    mysql.connection.commit()
    cursor.close()
    flash("Producto actualizado correctamente")
    return redirect(url_for('inventario'))

@app.route('/eliminar_producto/<int:id>')
def eliminar_producto(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM productos WHERE idProducto=%s', (id,))
    mysql.connection.commit()
    cursor.close()
    flash('Producto eliminado correctamente')
    return redirect(url_for('inventario'))

@app.route('/categorias', methods=['GET','POST'])
def categorias():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM categorias")
    categorias = cursor.fetchall()
    cursor.close()
    return render_template('categorias.html', categorias=categorias)

@app.route('/agregar_categorias', methods=['GET','POST'])
def agregar_categorias():
    if request.method=='POST':
        nombre=request.form['nombre']
        descripcion=request.form['descripcion']
        imagen=request.files['imagen']

        
        filename=secure_filename(imagen.filename)
        imagen.save(os.path.join('static/categorias',filename))
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO categorias (nombre,descripcion,imagen)VALUES(%s,%s,%s)",(nombre,descripcion,filename))
        mysql.connection.commit()
        cursor.close()

        flash("categoria almacenada correctamente")
        return redirect(url_for('categorias'))
    return render_template('agregar_categorias.html')

@app.route('/editar_categoria/<int:id>', methods=['POST'])
def editar_categoria (id):   
    nombre=request.form['nombre']
    descripcion=request.form['descripcion']
    imagen=request.files['imagen']
    cursor= mysql.connection.cursor()
    
    if imagen and imagen.filename != '':
        filename = secure_filename(imagen.filename)
        imagen.save(os.path.join('static/categorias', filename))
        cursor.execute("""
                       UPDATE categorias
                       SET nombre=%s, descripcion=%s, imagen=%s
                       WHERE idCategorias=%s
                       """, (nombre, descripcion, imagen, filename, id))
    else:
        cursor.execute("""
                       UPDATE categorias
                       SET nombre=%s, descripcion=%s, imagen=%s
                       WHERE idCategorias=%s
                       """, (nombre, descripcion,imagen , id))
    mysql.connection.commit()
    cursor.close()
    flash("categoria actualizado correctamente")
    return redirect(url_for('categoria'))
    
@app.route('/eliminar_categoria/<int:id>')
def eliminar_categoria(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM categorias WHERE idCategoria=%s', (id,))
    mysql.connection.commit()
    cursor.close()
    flash('categoria eliminado correctamente')
    return redirect(url_for('categoria'))
#fin inventario
    
def verificar_productos_vencimiento():
    """Revisa productos con fecha de vencimiento cercana y envía alerta."""
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    hoy = datetime.now().date()
    fecha_alerta = hoy + timedelta(days=3)  # alerta si vencen en 3 días
    cursor.execute("SELECT nombre_producto, fecha_vencimiento FROM productos WHERE fecha_vencimiento <= %s", (fecha_alerta,))
    productos = cursor.fetchall()
    cursor.close()

    if productos:
        mensaje = "*Alerta de productos próximos a vencer:*\n"
        for p in productos:
            mensaje += f"- {p['nombre_producto']} (vence {p['fecha_vencimiento']})\n"
        enviar_alerta_whatsapp(mensaje)
    else:
        print("No hay productos próximos a vencer.")


def tarea_alerta_vencimiento():
    """Ejecuta la verificación automática cada 24 horas."""
    while True:
        with app.app_context():
            print("Ejecutando verificación de productos por vencer...")
            verificar_productos_vencimiento()
        # Esperar 24 horas (86400 segundos)
        time.sleep(86400)

if __name__ == '__main__':
    # 🔹 Primera ejecución al iniciar el servidor
    with app.app_context():
        verificar_productos_vencimiento()

    # 🔹 Inicia hilo en segundo plano para verificación diaria
    hilo = threading.Thread(target=tarea_alerta_vencimiento, daemon=True)
    hilo.start()

    # 🔹 Ejecuta el servidor Flask
    app.run(port=5000, debug=True)



    

