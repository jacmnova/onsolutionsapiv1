from sqlalchemy.orm import sessionmaker
from models import Solicitud, Usuarios
from crud import engine
from sqlalchemy import func
import psycopg2
import datetime
import pytz
from random import choice
import emails


conn = psycopg2.connect(host="ec2-54-83-21-198.compute-1.amazonaws.com",
                         database="d8c40jdrkmkfl3",
                         user="nnkywspskxflte",
                         password="647cbdbaeaf2f1c050da08048ed5715b842a496df69b41b84e6af16577028154")


#Session on BD
Session = sessionmaker(bind=engine)

def insert_solicitudes(data):

    caracas = datetime.datetime.now(pytz.timezone('America/Caracas'))
    s = Session()
    solicitud = Solicitud(
        nombre=data['nombre'],
        apellido=data['apellido'],
        cedula=data['cedula'],
        email=data['email'],
        telefono=data['telefono'],
        tipo_afiliacion=data['tipoAfiliacion'],
        estado_afiliacion='NUEVA',
        fecha=caracas
    )
    s.add(solicitud)
    s.commit()
    s.close()
    return True


def get_solicitudes():
    s = Session()
    data = s.query(Solicitud).all()
    data = list(map(lambda x: x.serialize(), data))

    return data

def get_user_info(info):
    print(info)
    con = conn.cursor()
    con.execute("""SELECT id, usuario, tipo_usuario FROM public.usuarios WHERE usuario = %s and clave = %s;""",
                (info['user'], info['clave']))
    rs = con.fetchall()


    con.close()
    print(rs)
    if len(rs) > 0:
        aux = {}
        for row in rs:
            con = conn.cursor()
            con.execute("""SELECT id, plan_individual, plan_banca_asistencia, plan_corporativo 
                        FROM public.planes_usuarios WHERE id =""" + str(row[0]))
            info_ = con.fetchone()
            con.close()
            if info_ is not None:
                aux = {
                    'id': row[0],
                    'usuario': row[1],
                    'tipo_usuario': row[2],
                    'plan_individual': info_[0],
                    'plan_banca_asistencia': info_[1],
                    'plan_corporativo': info_[2],
                }
            else:
                aux = {
                    'id': row[0],
                    'usuario': row[1],
                    'tipo_usuario': row[2],
                    'plan_individual': '',
                    'plan_banca_asistencia': '',
                    'plan_corporativo': '',
                }
            print(aux)
        return aux
    else:
        return False

def denegar(id):
    caracas = datetime.datetime.now(pytz.timezone('America/Caracas'))
    cur = conn.cursor()
    cur.execute("""UPDATE public.solicitud SET estado_afiliacion='DENEGADA', fecha =%s WHERE id = %s""", (caracas, id))
    conn.commit()
    cur.close()

def aprobar(id):
    caracas = datetime.datetime.now(pytz.timezone('America/Caracas'))
    cur = conn.cursor()
    cur.execute("""UPDATE public.solicitud SET estado_afiliacion='APROBADA', fecha =%s WHERE id = %s""", (caracas, id))
    conn.commit()

    cur.execute("""SELECT nombre, apellido, cedula, email, telefono, tipo_afiliacion, estado_afiliacion 
                FROM public.solicitud WHERE id =  """ + str(id))
    data = cur.fetchone()

    cur.execute("""SELECT * FROM public.usuarios where usuario = '""" + data[3] + """'""")
    info_user = cur.fetchone()
    if info_user is None:
        longitud = 6
        valores = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

        p = ""
        p = p.join([choice(valores) for i in range(longitud)])
        cur.execute("""INSERT INTO public.usuarios(usuario, clave, tipo_usuario) VALUES(%s, %s, %s);""",
                    (data[3], p, 'CLIENT'))
        conn.commit()

        emails.send_mail(p, data[3], data[0], '')

        cur.execute("SELECT id FROM public.usuarios WHERE usuario = '" + data[3] + "'")
        id_user = cur.fetchone()


        if data[5] == 'INDIVIDUAL':
            cur.execute("""INSERT INTO public.planes_usuarios (id, plan_individual, plan_banca_asistencia, plan_corporativo)
                        VALUES("""+str(id_user[0])+""", true, false, false); """)
            conn.commit()
        if data[5] == 'BANCA-ASISTENCIA':
            cur.execute("""INSERT INTO public.planes_usuarios (id, plan_individual, plan_banca_asistencia, plan_corporativo)
                        VALUES(""" + str(id_user[0]) + """, true, false, false); """)
            conn.commit()
        if data[5] == 'CORPORATIVO':
            cur.execute("""INSERT INTO public.planes_usuarios (id, plan_individual, plan_banca_asistencia, plan_corporativo)
                        VALUES(""" + str(id_user[0]) + """, true, false, false); """)
            conn.commit()

    else:
        id_user = info_user[0]
        if data[5] == 'INDIVIDUAL':
            cur.execute("""UPDATE public.planes_usuarios SET plan_individual = true WHERE id= """ + str(id_user))
            conn.commit()
        if data[5] == 'BANCA-ASISTENCIA':
            cur.execute("""UPDATE public.planes_usuarios SET plan_banca_asistencia = true WHERE id= """ + str(id_user))
            conn.commit()
        if data[5] == 'CORPORATIVO':
            cur.execute("""UPDATE public.planes_usuarios SET plan_corporativo = true WHERE id= """ + str(id_user))
            conn.commit()


    cur.close()






    # all_people = Usuarios.query.filter_by(usuario=info['user'], clave=info['clave'])
    # all_people = list(map(lambda x: x.serialize(), all_people))
    # print(all_people)
    # return True