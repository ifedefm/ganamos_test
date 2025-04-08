import requests
import os
import pandas as pd
import streamlit as st
from funciones_ganamos import *
from typing import Tuple, Dict
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import datetime
import time

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

import requests

def login_ganamos(usuario, contrasenia):
    session = requests.Session()

    # 1. Hacer un GET inicial para establecer cookies base
    session.get("https://agents.ganamos.bet")

    # 2. Preparar headers y payload de login
    url_login = "https://agents.ganamos.bet/api/user/login"
    data = {
        "username": usuario,
        "password": contrasenia
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # 3. Hacer el POST de login
    response = session.post(url_login, json=data, headers=headers)

    if response.status_code != 200:
        print("⚠️ Código de respuesta:", response.status_code)
        print("🔍 Respuesta:", response.content)
        raise Exception(f"Login fallido: {response.status_code}")

    if "session" not in session.cookies:
        raise Exception("No se encontró la cookie de sesión")

    session_id = session.cookies.get("session")

    # 4. Usar la sesión autenticada para obtener info del usuario
    url_check = "https://agents.ganamos.bet/api/user/check"
    response_check = session.get(url_check)

    if response_check.status_code != 200:
        raise Exception("Error al verificar sesión")

    parent_id = response_check.json()['result']['id']

    # 5. Obtener lista de usuarios del agente
    url_users = 'https://agents.ganamos.bet/api/agent_admin/user/'
    params_users = {
        'count': '10',
        'page': '0',
        'user_id': parent_id,
        'is_banned': 'false',
        'is_direct_structure': 'false'
    }

    response_users = session.get(url_users, params=params_users)

    if response_users.status_code != 200:
        raise Exception("Error al obtener usuarios")

    lista_usuarios = {
        x['username']: x['id']
        for x in response_users.json()["result"]["users"]
    }

    return lista_usuarios, session_id



def carga_ganamos(alias: str, monto: float) -> tuple[bool, float]:
    """Versión optimizada para cargar saldo replicando navegador"""
    try:
        logger.info(f"Iniciando carga de saldo para {alias}")
        
        # Configurar sesión con reintentos
        session = requests.Session()
        retries = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["POST", "GET"]
        )
        session.mount('https://', HTTPAdapter(max_retries=retries))

        # 1. Obtener credenciales
        usuarios, session_id = login_ganamos('adminflamingo', '1111aaaa')
        
        # 2. Verificar usuario
        if alias not in usuarios:
            logger.error(f"Usuario {alias} no encontrado")
            return False, 0.0
            
        user_id = usuarios[alias]

        # 3. Configurar headers para la carga
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "es-419,es;q=0.9,en;q=0.8,pt;q=0.7,it;q=0.6",
            "priority": "u=1, i",
            "referer": "https://agents.ganamos.bet/",
            "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            "cookie": f"session={session_id}"
        }

        # 4. Realizar la carga
        payment_url = f"https://agents.ganamos.bet/api/agent_admin/user/{user_id}/payment/"
        payment_data = {"operation": 0, "amount": float(monto)}
        
        logger.info(f"Enviando carga a {payment_url}")
        response = session.post(
            payment_url,
            json=payment_data,
            headers=headers,
            timeout=15
        )
        
        if response.status_code != 200:
            error_msg = response.json().get('error_message', 'Error desconocido')
            raise Exception(f"Error en carga ({response.status_code}): {error_msg}")

        # 5. Verificar balance
        balance_url = "https://agents.ganamos.bet/api/user/balance"
        time.sleep(2)  # Esperar para asegurar actualización
        balance_response = session.get(balance_url, headers=headers, timeout=10)
        
        balance = 0.0
        if balance_response.status_code == 200:
            balance = balance_response.json().get("result", {}).get("balance", 0.0)
            logger.info(f"Balance actualizado: {balance}")
        
        return True, balance

    except Exception as e:
        logger.error(f"Error en carga_ganamos: {str(e)}")
        return False, 0.0
'''
#DESDE AQ CARGA_GANAMOS
def carga_ganamos(alias, monto):
    session = requests.Session()
    usuarios, session_id= login_ganamos()
    id_usuario = usuarios[alias]
    url_carga_ganamos = f'https://agents.ganamos.bet/api/agent_admin/user/{id_usuario}/payment/'

    payload_carga = {"operation":0,
                    "amount":monto}


    header_carga = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "es-419,es;q=0.9,en;q=0.8,pt;q=0.7,it;q=0.6",
    "priority": "u=1, i",
    "referer": "https://agents.ganamos.bet/",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    'cookie': f'session={session_id}'
    }

    response_carga_ganamos = session.post(url_carga_ganamos,json=payload_carga,headers=header_carga, cookies={'session':session_id})
    
    url_balance = 'https://agents.ganamos.bet/api/user/balance'
    header_check= {"accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "es-419,es;q=0.9,en;q=0.8,pt;q=0.7,it;q=0.6",
    "priority": "u=1, i",
    "referer": "https://agents.ganamos.bet/",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    'cookie': f'session={session_id}'
    }
    response_balance = session.get(url_balance, headers=header_check)
    balance_ganamos = response_balance.json()['result']['balance']
    if response_carga_ganamos.json()['error_message'] is None:
        return True, balance_ganamos
    else:
         return False , balance_ganamos
'''

#Desde aq todo igual
def retirar_ganamos(alias, monto):
    lista_usuarios, session_id= login_ganamos()
    id_usuario = lista_usuarios[alias]
    url_carga_ganamos = f'https://agents.ganamos.bet/api/agent_admin/user/{id_usuario}/payment/'

    payload_carga = {"operation":1,
                    "amount":monto}


    header_retiro = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "es-419,es;q=0.9,en;q=0.8,pt;q=0.7,it;q=0.6",
    "priority": "u=1, i",
    "referer": "https://agents.ganamos.bet/",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    'cookie': f'session={session_id}'
    }
    response_carga_ganamos = requests.post(url_carga_ganamos,json=payload_carga,headers=header_retiro, cookies={'session':session_id})

    url_balance = 'https://agents.ganamos.bet/api/user/balance'
    header_check= {"accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "es-419,es;q=0.9,en;q=0.8,pt;q=0.7,it;q=0.6",
    "priority": "u=1, i",
    "referer": "https://agents.ganamos.bet/",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    'cookie': f'session={session_id}'
    }
    response_balance = requests.get(url_balance, headers=header_check)
    balance_ganamos = response_balance.json()['result']['balance']
    if response_carga_ganamos.json()['error_message'] is None:
        return True, balance_ganamos
    else:
         return False, balance_ganamos
    

def nuevo_jugador(nueva_contrasenia, nuevo_usuario):
    lista_usuarios, session_id = login_ganamos(usuario='adminflamingo', contrasenia='1111aaaa')
    print(session_id)

    url_nuevo_usuario = 'https://agents.ganamos.bet/api/agent_admin/user/'

    data = {
        "email": "a",
        "first_name": "a",
        "last_name": "a",
        "password": f"{nueva_contrasenia}",
        "role": 0,
        "username": f"{nuevo_usuario}"
    }

    header_check = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "es-419,es;q=0.9,en;q=0.8,pt;q=0.7,it;q=0.6",
        "priority": "u=1, i",
        "referer": "https://agents.ganamos.bet/",
        "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        'cookie': f'session={session_id}'
        }

    response = requests.post(url_nuevo_usuario, json=data, headers=header_check)
    if response.json()['status'] == 0:
        return 'Usuario creado',lista_usuarios,nueva_contrasenia,nuevo_usuario    
    if 'already exist' in response.json()['error_message']:
        return 'El usuario ya existe, Prueba con otro usuario',lista_usuarios
    

csv_file = 'data.csv'

def guardar_usuario(usuario, contraseña, email, telefono):
        
    if not usuario or not contraseña:
        st.warning('Debe ingresar un usuario y una contraseña.')
        return
    
    resultado, lista_usuarios = nuevo_jugador(nuevo_usuario=usuario, nueva_contrasenia=contraseña, usuario='adminflamingo', contrasenia='1111aaaa')
    
    if 'Usuario creado' in resultado:
        nuevo_dato = pd.DataFrame({'user': [usuario], 'password': [contraseña],'email': [email], 'telefono': [telefono]})
        
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            df = pd.concat([df, nuevo_dato], ignore_index=True)
        else:
            df = nuevo_dato
        
        df.to_csv(csv_file, index=False)
        st.success('Usuario creado!!!')
    else:
        st.warning(resultado)


