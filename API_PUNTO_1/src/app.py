from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import config


app = Flask(__name__)

conexion = MySQL(app)


@app.route('/cursos',  methods=['GET'])
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
        return jsonify({'cursos': usuarios, 'mensaje': "Usuarios listados"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})


@app.route('/cursos/<codigo>',  methods=['GET'])
def leer_Curso(codigo):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT codigo, nombre, creditos FROM curso WHERE codigo ='{0}'".format(
            codigo)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            curso = {'codigo': datos[0],
                     'nombre': datos[1], 'creditos': datos[2]}
            return jsonify({'cursos': curso, 'mensaje': "Curso listado"})
        else:
            return jsonify({'mensaje': "Curso no encontrado"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})

@app.route('/usuario/login/<correo>', methods=['GET'])
def login_usuario(correo):
    try:
        cursor = conexion.connection.cursor()
        sql="SELECT correo , contrasena FROM usuarios WHERE correo = '{0}'".format(correo)
        cursor.execute(sql)
        users= cursor.fetchone()
        print("aquiii"+users)
        if users != None:
            usuario = {'correo': usuario[0], 'contrasena': usuario[1]}
            return jsonify({'usuario': usuario, 'mensaje': "usuario listado"})
        else:
            return jsonify({'mensaje': "Curso no encontrado"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})




@app.route('/usuario', methods=['POST'])
def registrar_usuario():
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


@app.route('/cursos/<codigo>',  methods=['PUT'])
def actualizar_curso(codigo):
    try:
        cursor = conexion.connection.cursor()
        sql = "UPDATE curso SET nombre = '{0}', creditos = {1} WHERE codigo = '{2}'".format(
            request.json['nombre'], request.json['creditos'], codigo)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje': "Curso actualizado"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})
    


@app.route('/cursos/<codigo>', methods=['DELETE'])
def eliminar_cursos(codigo):
    try:
        # print(request.json)
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM curso WHERE codigo ='{0}'".format(codigo)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje': "Curso Eliminado"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})


def pagina_no_encontrada(error):
    return "<h1> La pagina que intentas buscar no existe...</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()