from flask import Flask, render_template, request, redirect,  url_for, flash
from flask_mysqldb import MySQL
#Aca ya estoy conectado en MySQL
app = Flask(__name__)

# MySQL Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskcontactos'
mysql = MySQL(app)

# Setting
app.secret_key = 'mysecretkey'

@app.route("/")
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contactos')
    data = cur.fetchall()
    return render_template('index.html', contactos=data)

@app.route('/agregar_contacto', methods=['POST'])
def agregar_contacto():
    if request.method == 'POST':
        nombre_completo = request.form['Nombre_Completo']
        telefono = request.form['Telefono']
        email = request.form['Email']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contactos (nombrecompleto, telefono, email) VALUES (%s, %s, %s)', (nombre_completo, telefono, email))
        mysql.connection.commit()
        flash('Contacto Agregado Perfectamente!')
        cur.close()
        return redirect(url_for('Index')) #No Envia un mensaje feo

@app.route('/editar/<id>')
def get_contactos(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contactos WHERE id = %s', (id,))
    data = cur.fetchall()
    return render_template('editar.html', contactos = data[0])

@app.route('/actualizar_contacto/<id>', methods=['POST'])
def actualizar_contacto(id):
    if request.method == 'POST':
        nombrecompleto = request.form['Nombre_Completo']
        telefono = request.form['Telefono']
        email = request.form['Email']
        
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contactos
            SET nombrecompleto = %s,
                telefono = %s,
                email = %s
            WHERE id = %s
        """, (nombrecompleto, telefono, email, id))
        
        mysql.connection.commit()
        flash('Contacto actualizado correctamente!')
        return redirect(url_for('Index'))

@app.route("/borrar/<string:id>")
def eliminar_contacto(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contactos WHERE id = {0}'.format(id,))
    mysql.connection.commit()
    flash('Contactos Removido Perfectamente')
    return redirect(url_for('Index'))



if __name__ == '__main__': 
    app.run(port = 3000, debug = True)