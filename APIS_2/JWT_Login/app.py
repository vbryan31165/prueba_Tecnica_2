from flask import Flask, jsonify, request
from flask import request
from flask_mysqldb import MySQL
from config import config
from function_jwt import write_token, validate_token

app = Flask(__name__)

conexion = MySQL(app)


@app.route('/usuarios/login', methods=['POST'])
def login_usuario():
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
            data = request.get_json()
            print("AQUI")
            print(type(data))
            return write_token(data=request.get_json())
        else:
            return jsonify({'mensaje': "Curso no encontrado"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})

@app.route("/verify/token")
def verify():
    token=request.headers['Authorization'].split(" ")[1]
    return validate_token(token, output=True)

@app.route('/usuarios', methods=['POST'])
def registrar_usuario():
    try:
        # print(request.json)
        cursor = conexion.connection.cursor()
        sql = "INSERT INTO usuarios ( nombreCompleto, correo, contrasena, direccion, telefono, fechaNacimiento) VALUES ('{0}', '{1}', '{2}','{3}','{4}','{5}')".format(
            request.json['nombreCompleto'], request.json['correo'], request.json['contrasena'], request.json['direccion'], request.json['telefono'], request.json['fechaNacimiento'],)
        cursor.execute(sql)
        # print("AQUI"+sql)
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