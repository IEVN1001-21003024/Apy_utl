from flask import Flask,request, jsonify
from flask_mysqldb import MySQL

from config import config

""" GET, POST, PUT , DELETE """

app=Flask(__name__)

con=MySQL(app)

@app.route("/alumnos",methods=['GET'])
def lista_alumnos():
    try:
        cursor=con.connection.cursor()
        sql="select * from alumnos"
        cursor.execute(sql)
        datos=cursor.fetchall()
        alumnos=[]
        for fila in datos:
            alumno={"matricula":fila[0], "nombre":fila[1], "apaterno":fila[2], "amaterno":fila[3], "correo":fila[4]}
            alumnos.append(alumno)
        return jsonify({'alumnos':alumnos,'mensaje':'Lista de alumnos', 'exito':True})
    except Exception as ex:
        return jsonify({"message": "error {}".format(ex),'exito':False}),500


def leer_alumno_bd(matricula):
    try:
        cursor=con.connection.cursor()
        sql="select * from alumnos where matricula={}".format(matricula)
        
        cursor.execute(sql)
        datos=cursor.fetchone()
        if datos!=None:
            alumno={"matricula":datos[0], "nombre":datos[1], "apaterno":datos[2], "amaterno":datos[3], "correo":datos[4]}
            return alumno
        else:    
            return None
          
    except Exception as ex:
        return jsonify({"message": "error {}".format(ex),'exito':False}),500


@app.route("/alumnos/<mat>",methods=['GET'])
def leer_alumno(mat):
    try:
        alumno=leer_alumno_bd(mat)
        if alumno!=None:
            return jsonify({'alumno':alumno,'mensaje':'Alumno encontrado', 'exito':True})
        else:
            return jsonify({'alumno':alumno,'mensaje':'Alumno no encontrado', 'exito':False})
        
    except Exception as ex:
        return jsonify({"message": "error {}".format(ex),'exito':False}),500
    

@app.route("/alumnos",methods=['POST'])
def registrar_alumno():
    try:
        alumno=leer_alumno_bd(request.json['matricula'])
        if alumno!=None:
            return jsonify({'mensaje':"alumno ya existente no se puede duplicar",'exito':False})
        else:
            cursor=con.connection.cursor()
            sql='insert into alumno(matricula,nombre,apaterno,amaterno,correo) values("{0}","{1}","{2}","{3}","{4}")'.format(request.json['matricula'],request.json['nombre'],request.json['apaterno'],request.json['amaterno'],request.json['correo'])
            cursor.execute(sql)
            con.connection.commit()
            return jsonify({'mensaje':"alumno registrado",'exito':True})
            
    except Exception as ex:
        return jsonify({"message": "error",'exito':False})

@app.route('/alumnos/<mat>', methods=['PUT'])
def actualizar_curso(mat):
    #if (validar_matricula(mat) and validar_nombre(request.json['nombre']) and validar_apaterno(request.json['apaterno'])):
        try:
            alumno = leer_alumno_bd(mat)
            if alumno != None:
                cursor = con.connection.cursor()
                sql = """UPDATE alumnos SET nombre = '{0}', apaterno = '{1}', amaterno='{2}', correo='{3}'
                WHERE matricula = {4}""".format(request.json['nombre'], request.json['apaterno'], request.json['amaterno'],request.json['correo'], mat)
                cursor.execute(sql)
                con.connection.commit()  # Confirma la acción de actualización.
                return jsonify({'mensaje': "Alumno actualizado.", 'exito': True})
            else:
                return jsonify({'mensaje': "Alumno no encontrado.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': "Error {0} ".format(ex), 'exito': False})
    #else:
     #   return jsonify({'mensaje': "Parámetros inválidos...", 'exito': False})
 
 
@app.route('/alumnos/<mat>', methods=['DELETE'])
def eliminar_curso(mat):
    try:
        alumno = leer_alumno_bd(mat)
        if alumno != None:
            cursor = con.connection.cursor()
            sql = "DELETE FROM alumnos WHERE matricula = {0}".format(mat)
            cursor.execute(sql)
            con.connection.commit()  # Confirma la acción de eliminación.
            return jsonify({'mensaje': "Alumno eliminado.", 'exito': True})
        else:
            return jsonify({'mensaje': "Alumno no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})
    
def pagina_no_encontrada(error):
    return"<h1>Pagina no encontrada</h1>"    
if __name__=="__main__":
    app.config.from_object(config['development'])
    app.register_error_handler(404,pagina_no_encontrada)
    app.run(host='0.0.0.0',port=5000)