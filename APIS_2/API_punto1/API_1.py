
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import config

app = Flask(__name__)

conexion = MySQL(app)


@app.route('/usuarios',  methods=['GET'])
def listar_usuarios():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM usuarios"
        cursor.execute(sql)
        datos = cursor.fetchall()
        usuarios = []
        for fila in datos:
            curso = {'nombreCompleto': fila[1], 'Correo': fila[2]}
            usuarios.append(curso)
        return jsonify({'Usuarios': usuarios, 'mensaje': "Usuarios listados"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})

@app.route('/usuarios/login', methods=['POST'])
def login_usuarios():
    try:
        # print(request.json)
        cursor = conexion.connection.cursor()

        sql = "SELECT correo , contrasena FROM usuarios WHERE correo = '{0}' AND contrasena = {1}".format(
            request.json['correo'], request.json['contrasena'])
        cursor.execute(sql)
        print(sql)
        users = cursor.fetchone()
        print("hola")
        print(users)
        if users != None:
            usuario = {'correo': users[0], 'contrasena': users[1]}
            return jsonify({'usuario : ': usuario, 'mensaje':'Usuario iniciado correctamente'})
        else:
            return jsonify({'mensaje': "usuario o contraseña incorrecta"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})


@app.route('/usuarios/registrar',  methods=['POST'])
def registrar_usuarios():
    try:
        #print(request.json)
        cursor = conexion.connection.cursor()
        sql = "INSERT INTO usuarios ( nombreCompleto, correo, contrasena, direccion, telefono, fechaNacimiento) VALUES ('{0}', '{1}', '{2}','{3}','{4}','{5}')".format(
            request.json['nombreCompleto'], request.json['correo'], request.json['contrasena'], request.json['direccion'], request.json['telefono'], request.json['fechaNacimiento'],)
        cursor.execute(sql)
        #print("AQUI"+sql)
        conexion.connection.commit()
        return jsonify({'mensaje': "Usuario registrado"})
    
    except Exception as ex:
        return jsonify({'mensaje': "Error"})


def pagina_no_encontrada(error):
    return "<h1> La pagina que intentas buscar no existe...</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()