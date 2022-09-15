from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import config


app = Flask(__name__)

conexion = MySQL(app)


@app.route('/productos/listar',  methods=['GET'])
def listar_productos():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM productos"
        cursor.execute(sql)
        datos = cursor.fetchall()
        # print(datos)
        productos = []
        # print(noticias)
        for fila in datos:
            print(fila)
            datos = {'1id': fila[0], '2nombre': fila[1],
                     '3valor': fila[2], '4cantidad': fila[3]}
            productos.append(datos)
        return jsonify({'Productos': productos, 'mensaje': "productos listados"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})

@app.route('/productos/registrar', methods=['POST'])
def registrar_producto():
    try:
        print(request.json)
        cursor = conexion.connection.cursor()
        sql = "INSERT INTO productos (nombre, valor, cantidad) VALUES ('{0}', '{1}','{2}')".format(
            request.json['nombre'], request.json['valor'], request.json['cantidad'])
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje': "producto registrado"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})



@app.route('/compra/producto', methods=['POST'])
def comprar_producto():
  try:
      id_producto = request.json['id_producto']
      existencias =  existenciasBD(id_producto)
      cantidad = request.json['cantidad']
      if (existencias != False) and (existencias[3] > 0) and (existencias[3] > cantidad):
          precio = existencias[2] * cantidad
          nameComprador = request.json['nombreComprador']
          
          cursor = conexion.connection.cursor()
          cursor.execute('INSERT INTO compras (id_producto, cantidad, precio, nombreComprador) VALUES (%s,%s,%s, %s)',(id_producto, cantidad,precio,nameComprador))
          cursor.connection.commit()
          
          resta = existencias[3] - cantidad
          
          if restar_CantidadBD(id_producto, resta):
              return jsonify({'Mensaje: ': 'Producto comprado exitosamente!!'})
          else:
              return jsonify({'Error': 'Oops!!! no se ha podido ingregar la compra'})
      else:
          return jsonify({'advertencia': 'Producto no tiene mas cantidad en el inventario!!'})
  except:
        return jsonify({'Error': 'Oops!!! ha ocurrido un error'})


def restar_CantidadBD(id_product, resta):
    try:
        cursor = conexion.connection.cursor()
        cursor.execute('UPDATE productos SET cantidad = %s WHERE productos.id = %s', (resta, id_product))
        cursor.connection.commit()
        return True    
    except:
        return False


def existenciasBD(id_producto):
    try:
        cursor = conexion.connection.cursor()
        cursor.execute('SELECT * FROM productos WHERE id = %s',(id_producto,))
        value = cursor.fetchone()
        
        if value != None:
          return value
        else:
          return False
    
    except:
          return jsonify({'Error': 'You must send a valid id'})


@app.route('/productos/actualizar/<codigo>',  methods=['PUT'])
def actualizar_producto(codigo):
    try:
        cursor = conexion.connection.cursor()
        sql = "UPDATE productos SET nombre = '{0}', valor = '{1}', cantidad='{2}' WHERE id = '{3}'".format(
            request.json['nombre'], request.json['valor'],request.json['cantidad'], codigo)
        print(sql)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje': "producto actualizado"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})

@app.route('/productos/eliminar/<codigo>', methods=['DELETE'])
def eliminar_noticia(codigo):
    try:
        # print(request.json)
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM productos WHERE id ='{0}'".format(codigo)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje': "Producto Eliminado"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})


def pagina_No_Encontrada(error):
    return "<h1> La pagina que intentas buscar no existe...</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_No_Encontrada)
    app.run()