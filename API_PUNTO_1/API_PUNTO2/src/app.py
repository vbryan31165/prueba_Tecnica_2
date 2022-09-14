from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import config


app = Flask(__name__)

conexion = MySQL(app)


@app.route('/noticias',  methods=['GET'])
def listar_noticias():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM noticias"
        cursor.execute(sql)
        datos = cursor.fetchall()
        #print(datos)
        noticias_ = []
        #print(noticias)
        for fila in datos:
            print(fila)
            datos = {'1id': fila[0], '2titulo': fila[1], 'descripcion': fila[2]}
            noticias_.append(datos)
        return jsonify({'cursos': noticias_, 'mensaje': "noticias listados"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})


@app.route('/noticias/registrar', methods=['POST'])
def registrar_noticia():
    try:
        print(request.json)
        cursor = conexion.connection.cursor()
        sql = "INSERT INTO noticias (titulo, descripcion) VALUES ('{0}', '{1}')".format(
            request.json['titulo'], request.json['descripcion'])
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje': "Noticia registrada"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})


@app.route('/noticias/actualizar/<codigo>',  methods=['PUT'])
def actualizar_noticia(codigo):
    try:
        cursor = conexion.connection.cursor()
        sql = "UPDATE noticias SET titulo = '{0}', descripcion = {1} WHERE id = '{2}'".format(
            request.json['titulo'], request.json['descripcion'], codigo)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje': "noticia actualizada"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})


@app.route('/noticias/<codigo>', methods=['DELETE'])
def eliminar_noticia(codigo):
    try:
        # print(request.json)
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM noticias WHERE id ='{0}'".format(codigo)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje': "noticia Eliminado"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})


def pagina_no_encontrada(error):
    return "<h1> La pagina que intentas buscar no existe...</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()