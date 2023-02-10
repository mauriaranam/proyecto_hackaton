#Importamos las librerias
from flask import Flask, request, render_template, redirect,url_for
from flask_sqlalchemy import SQLAlchemy


#Creamos una app flask
app = Flask(__name__)
#Creamos el modelo de la db del usuario

app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base_de_datos.db'
app.config ['SECRET_KEY'] = 'puni77'

#Creamos la base de datos
db = SQLAlchemy(app)

#Platillas para crear objetos
#Datos para qpoder meter en la db

#BASE DE DATOS DE USUARIO
class Usuario (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    #Creamos el constructor de clase
    def __init__ (self,nombre, email, password):
        self.nombre = nombre
        self.email = email
        self.password = password

#FICHA DEL USUARIO
class Ficha (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    nombre_completo = db.Column(db.String(50), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    peso = db.Column(db.Float, nullable=False)
    estatura = db.Column(db.Float, nullable=False)
    ci = db.Column(db.Integer, nullable=False)
    tipo_de_sangre = db.Column(db.String(10)) 

    def __init__ (self,nombre_completo, edad, peso, estatura, ci, id_usuario, tipo_de_sangre):
        self.nombre_completo = nombre_completo
        self.edad = edad
        self.peso = peso
        self.estatura = estatura
        self.ci = ci
        self.id_usuario = id_usuario
        self.tipo_de_sangre = tipo_de_sangre


#BASE DE DATOS DE CONSULTAS
class Consultas (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # usuario se refiere a la clase 
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    doctor = db.Column(db.String(30), nullable=False)
    hora = db.Column(db.String, nullable=False)
    fecha = db.Column(db.String, nullable=False)
    motivo = db.Column(db.String(30), nullable=False)

    #Creamos el constructor de clase
    def __init__ (self,doctor, hora, fecha, motivo, id_usuario):
        self.doctor = doctor
        self.hora = hora
        self.fecha = fecha
        self.motivo = motivo
        self.id_usuario = id_usuario

class Recetas (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    medicamento = db.Column(db.String(35), nullable=False)
    motivo = db.Column(db.String, nullable=False)
    fecha_de_inicio = db.Column(db.String(30), nullable=False)
    hora_inicio_toma = db.Column(db.String(30), nullable=False)
    hora_entre_cada_toma = db.Column(db.String(3), nullable=False)
    dias_a_tomar = db.Column(db.String(5), nullable=False)
    
    def __init__ (self,medicamento, motivo, fecha_de_inicio, hora_inicio_toma, hora_entre_cada_toma, dias_a_tomar, id_usuario):
        self.medicamento = medicamento
        self.motivo = motivo
        self.fecha_de_inicio = fecha_de_inicio
        self.hora_inicio_toma = hora_inicio_toma
        self.hora_entre_cada_toma = hora_entre_cada_toma
        self.dias_a_tomar = dias_a_tomar
        self.id_usuario = id_usuario
    


#Creamos la base de datos y siempre va debajo de la declaracion de clases
with app.app_context():
    db.create_all()

#Creamos una ruta para el login
#Get trae las cosas del back
#Post lleva las cosas al back
@app.route('/register', methods = ['GET', 'POST'])
def register():
    #Aca se reciben datos del front al back
    if request.method == 'POST':
        nombre_usuario = request.form ['username']
        email = request.form ['email']
        password = request.form ['password']
        #Creamos un objeto de la clase que creamos para el modelo de la base de datos 
        #Este objeto  puede ingresarse a la base de datos sin problemas
        usuario = Usuario(nombre_usuario, email, password)
        #Agregar a la DB
        #Quiero agregar algo y 
        db.session.add(usuario)
        #Confirmo con el commit
        db.session.commit()

        global current_user
        current_user = usuario.id 
        return redirect(url_for('ficha'))
    return render_template('register.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form ['email']
        password = request.form ['password']
        usuario_db = Usuario.query.filter_by(email=email).first()
        if usuario_db is not None:
            if usuario_db.password == password:
                global current_user 
                current_user = usuario_db.id
                return redirect(url_for('home'))
            else:
                return redirect(url_for('login'))
        elif usuario_db is None:
            return redirect(url_for('login'))  
    return render_template('login.html')

@app.route('/ficha', methods = ['GET', 'POST'])
def ficha():
    #Aca se reciben datos del front al back
    if request.method == 'POST':
        nombre_completo = request.form ['nombre_completo']
        edad = request.form ['edad']
        peso = request.form ['peso']
        estatura = request.form ['estatura']
        ci = request.form ['ci']
        tipo_de_sangre = request.form ['tipo_de_sangre']

        global current_user 
        id_usuario = current_user

        ficha_de_usuario = Ficha(nombre_completo, edad, peso, estatura, ci, id_usuario, tipo_de_sangre)
        db.session.add(ficha_de_usuario)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('ficha.html')

@app.route('/consultas', methods = ['GET', 'POST'])
def consultas():
    if request.method == 'POST':
        doctor = request.form ['doctor']
        hora = request.form ['hora']
        fecha = request.form ['fecha']
        motivo = request.form ['motivo']

        global current_user 
        id_usuario = current_user

        agregar_consultas = Consultas(doctor, hora, fecha, motivo, id_usuario)
        db.session.add(agregar_consultas)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('consultas.html')

@app.route('/medicacion', methods = ['GET', 'POST'])
def medicacion():
    if request.method == 'POST':
        # print('aaaaaaaaaaaaaaaaaaaaaaaa')
        medicamento = request.form ['medicamento']
        hora_inicial_de_toma = request.form ['hora_inicial']
        cada_hora_a_tomar = request.form ['cada_hora']
        motivo = request.form['motivo']
        dias_a_tomar = request.form['dias_a_tomar']

        global current_user 
        id_usuario = current_user

        agregar_medicacion = Recetas(medicamento, motivo, hora_inicial_de_toma, hora_inicial_de_toma, cada_hora_a_tomar, dias_a_tomar, id_usuario)
        db.session.add(agregar_medicacion)
        db.session.commit()

        lista_horarios = receta(int(hora_inicial_de_toma), int(cada_hora_a_tomar))
        print(lista_horarios)
        return redirect(url_for('home'))
    return render_template('medicacion.html')

def receta(hora_inicial_de_toma, cada_hora_a_tomar):
    lista = []
    cantidad_recorrida = int(24 / cada_hora_a_tomar)
    hora_a_tomar = hora_inicial_de_toma

    for veces in range (cantidad_recorrida):
        hora_a_tomar = hora_a_tomar + cada_hora_a_tomar
        # Validar para que no salga 35 horas 
        if hora_a_tomar > 24: 
            hora_a_tomar = hora_a_tomar - 24 
        lista.append(hora_a_tomar)
    return lista 

@app.route ('/home')
def home ():
    # Buscar todas las consultas de ese usuario 
    query_consultas = Consultas.query.filter_by(id_usuario = current_user).all()
    # print(consultas[0].doctor)

    return render_template('pagina_principal.html', consultas=query_consultas)

if __name__ == '__main__': 
    current_user = None 
    app.run (debug=True)


@app.route('/agenda', methods = ['GET', 'POST'])
def agenda():
    # Buscar todas las consultas de ese usuario 
    query_consultas = Consultas.query.filter_by(id_usuario = current_user).all()
    # print(consultas[0].doctor)
    return render_template('pagina_principal.html', consultas=query_consultas)
    
        




