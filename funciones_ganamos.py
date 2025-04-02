import requests
import os
import pandas as pd
import streamlit as st
from funciones_ganamos import *
import time
from typing import Tuple, Dict
'''
def login_ganamos():
    
    session = requests.Session()
    
    url = 'https://agents.ganamos.bet/api/user/login'

    data = {
        "password": '1111aaaa',
        "username": 'adminflamingo'    
    }

    headers = {
        "authority": "agents.ganamos.bet",
        "method": "POST",
        "path": "/api/user/login",
        "scheme": "https",
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Content-Length": "50",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://agents.ganamos.bet",
        "Pragma": "no-cache",
        "Referer": "https://agents.ganamos.bet/",
        "Sec-Ch-Ua": "\"Not A(Brand\";v=\"99\", \"Google Chrome\";v=\"121\", \"Chromium\";v=\"121\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }

    response = session.post(url, json=data, headers=headers)
    
    if response.status_code == 200 and "session" in response.cookies:
        session_id = response.cookies["session"]
    else:
        raise Exception("Error en el login: No se pudo obtener session_id")
    
    # Continúa con el código solo si session_id fue obtenido correctamente
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

    url_check = "https://agents.ganamos.bet/api/user/check"
    response_check = session.get(url_check, headers=header_check)
    
    if response_check.status_code != 200:
        raise Exception("Error en la verificación de usuario.")

    parent_id = response_check.json()['result']['id']
    
    url_users = 'https://agents.ganamos.bet/api/agent_admin/user/'
    params_users = {
        'count': '10',
        'page': '0',
        'user_id': parent_id,
        'is_banned': 'false',
        'is_direct_structure': 'false'
    }
    response_users = session.get(url_users, params=params_users, headers=header_check)

    if response_users.status_code != 200:
        raise Exception("Error obteniendo lista de usuarios.")

    lista_usuarios = {x['username']: x['id'] for x in response_users.json()["result"]["users"]}
    
    return lista_usuarios, session_id

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
import requests
import time
from typing import Tuple, Dict

def login_ganamos() -> Tuple[Dict[str, int], str]:
    """
    Función optimizada de login con manejo de errores mejorado
    
    Returns:
        Tuple[Dict[str, int], str]: Diccionario de usuarios y session_id
        
    Raises:
        Exception: Si falla el login después de 3 intentos
    """
    # Configuración (debería estar en variables de entorno)
    LOGIN_URL = 'https://agents.ganamos.bet/api/user/login'
    CREDENTIALS = {
        'username': 'adminflamingo',
        'password': '1111aaaa'
    }
    
    # Headers optimizados
    HEADERS = {
        "accept": "application/json",
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
    }
    
    for attempt in range(3):
        try:
            # 1. Realizar login
            response = requests.post(
                LOGIN_URL,
                json=CREDENTIALS,
                headers=HEADERS,
                timeout=10
            )
            
            if response.status_code != 200:
                raise ValueError(f"Error en login: {response.status_code}")
                
            session_id = response.cookies.get("session")
            if not session_id:
                raise ValueError("No se recibió session_id")
                
            # 2. Verificar sesión
            CHECK_URL = 'https://agents.ganamos.bet/api/user/check'
            check_response = requests.get(
                CHECK_URL,
                headers={**HEADERS, "cookie": f"session={session_id}"},
                timeout=10
            )
            
            if check_response.status_code != 200:
                raise ValueError("Error en verificación de sesión")
                
            parent_id = check_response.json()['result']['id']
            
            # 3. Obtener lista de usuarios
            USERS_URL = 'https://agents.ganamos.bet/api/agent_admin/user/'
            users_response = requests.get(
                USERS_URL,
                params={
                    'count': '1000',  # Obtener todos los usuarios
                    'page': '0',
                    'user_id': parent_id,
                    'is_banned': 'false',
                    'is_direct_structure': 'false'
                },
                headers={**HEADERS, "cookie": f"session={session_id}"},
                timeout=10
            )
            
            if users_response.status_code != 200:
                raise ValueError("Error obteniendo usuarios")
                
            users = users_response.json()
            lista_usuarios = {
                user['username']: user['id'] 
                for user in users["result"]["users"]
            }
            
            return lista_usuarios, session_id
            
        except Exception as e:
            if attempt == 2:  # Último intento
                raise Exception(f"Fallo de login después de 3 intentos: {str(e)}")
            time.sleep(3)  # Esperar antes de reintentar

def carga_ganamos(alias: str, monto: float) -> Tuple[bool, float]:
    """
    Función optimizada para cargar saldo con manejo robusto de errores
    
    Args:
        alias: Nombre de usuario
        monto: Monto a cargar
        
    Returns:
        Tuple[bool, float]: (éxito, balance actual)
    """
    try:
        # 1. Obtener credenciales frescas
        usuarios, session_id = login_ganamos()
        
        if alias not in usuarios:
            raise ValueError(f"Usuario {alias} no encontrado")
            
        # 2. Configurar petición de carga
        PAYMENT_URL = f'https://agents.ganamos.bet/api/agent_admin/user/{usuarios[alias]}/payment/'
        BALANCE_URL = 'https://agents.ganamos.bet/api/user/balance'
        
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "cookie": f"session={session_id}",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
        }
        
        # 3. Realizar carga
        payload = {"operation": 0, "amount": float(monto)}
        response = requests.post(
            PAYMENT_URL,
            json=payload,
            headers=headers,
            timeout=10
        )
        
        if response.status_code != 200:
            error_msg = response.json().get('error_message', 'Error desconocido')
            raise ValueError(f"Error en carga: {error_msg}")
            
        # 4. Obtener balance
        balance_response = requests.get(BALANCE_URL, headers=headers, timeout=10)
        balance = balance_response.json()['result']['balance'] if balance_response.status_code == 200 else 0.0
        
        return True, balance
        
    except Exception as e:
        # Registrar el error para diagnóstico
        print(f"Error en carga_ganamos: {str(e)}")
        return False, 0.0

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
    lista_usuarios, session_id= login_ganamos('adminflamingo','1111aaaa')
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
        return 'Usuario creado',lista_usuarios    
    if 'already exist' in response.json()['error_message']:
        return 'El usuario ya existe, Prueba con otro usuario',lista_usuarios
    

csv_file = 'data.csv'

def guardar_usuario(usuario, contraseña):
        
    if not usuario or not contraseña:
        st.warning('Debe ingresar un usuario y una contraseña.')
        return
    
    resultado, lista_usuarios = nuevo_jugador(nuevo_usuario=usuario, nueva_contrasenia=contraseña, usuario='adminflamingo', contrasenia='1111aaaa')
    
    if 'Usuario creado' in resultado:
        nuevo_dato = pd.DataFrame({'user': [usuario], 'password': [contraseña]})
        
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            df = pd.concat([df, nuevo_dato], ignore_index=True)
        else:
            df = nuevo_dato
        
        df.to_csv(csv_file, index=False)
        st.success('Usuario creado!!!')
    else:
        st.warning(resultado)


