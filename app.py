from logging import debug
from flask import Flask, render_template, request, redirect, flash
from flask.helpers import url_for
from flaskext.mysql import MySQL

app=Flask(__name__)
app.secret_key="dev"

mysql= MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']='root'
app.config['MYSQL_DATABASE_DB']='sistema'
mysql.init_app(app)

@app.route('/')
def index():
    sql="SELECT * FROM empleados;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    empleados=cursor.fetchall()
    conn.commit()
    return render_template('empleados/index.html', empleados=empleados)

@app.route('/delete/<int:id>')
def delete(id):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM empleados WHERE id=%s",(id))
    conn.commit()
    return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM empleados WHERE id=%s",(id))
    empleados=cursor.fetchall()
    conn.commit()
    return render_template('empleados/edit.html', empleados=empleados)

@app.route('/update', methods=['POST'])
def update():
    _nombre=request.form['txtNombre']
    _apellido=request.form['txtApellido']
    _correo=request.form['txtCorreo']
    _telefono=request.form['txtTelefono']
    id=request.form['txtID']
    sql="UPDATE empleados SET nombre=%s, apellido=%s, correo=%s, telefono=%s WHERE id=%s"
    datos =(_nombre,_apellido,_correo,_telefono,id)
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/')
    

@app.route('/create')
def create():
    return render_template('empleados/create.html')

@app.route('/store', methods=['POST'])
def storage():
    _nombre=request.form['txtNombre']
    _apellido=request.form['txtApellido']
    _correo=request.form['txtCorreo']
    _telefono=request.form['txtTelefono']
    if _nombre=='' or _correo=='' or _apellido=='' or _telefono=='':
        flash('No dejar campos vacios')
        return redirect(url_for('create'))
    sql="INSERT INTO empleados(nombre,apellido,correo,telefono) VALUES (%s,%s,%s,%s);"
    datos =(_nombre,_apellido,_correo,_telefono)
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/')

if __name__== '__main__':
    app.run(debug=True)