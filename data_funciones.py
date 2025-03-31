import streamlit as st
import pandas as pd
import os
from funciones_ganamos import login_ganamos, nuevo_jugador, carga_ganamos, retirar_ganamos
csv_file = 'data.csv'

def guardar_usuario(usuario, contraseña):
    usuario = usuario
    contraseña = contraseña
    nuevo_jugador(nuevo_usuario=usuario,
                  nueva_contrasenia=contraseña)
    
    if usuario and contraseña:
        nuevo_dato = pd.DataFrame({'user': [usuario], 'password': [contraseña]})
        
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            df = pd.concat([df, nuevo_dato], ignore_index=True)
        else:
            df = nuevo_dato
        
        df.to_csv(csv_file, index=False)
        st.success('Usuario creado correctamente y guardado en CSV.')
    else:
        st.warning('Debe ingresar un usuario y una contraseña.')