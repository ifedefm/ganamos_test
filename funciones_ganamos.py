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
def login_ganamos(max_retries: int = 3, retry_delay: int = 5) -> Tuple[Dict[str, int], str]:
    """
    Función mejorada de login con manejo robusto de errores y reintentos
    
    Args:
        max_retries: Número máximo de reintentos
        retry_delay: Segundos de espera entre reintentos
        
    Returns:
        Tuple con (diccionario de usuarios, session_id)
        
    Raises:
        Exception: Si falla después de max_retries intentos
    """
    # Configuración de credenciales (deberían estar en variables de entorno)
    CREDENTIALS = {
        'username': 'adminflamingo',
        'password': '1111aaaa'
    }
    
    # URLs del API
    URLS = {
        'login': 'https://agents.ganamos.bet/api/user/login',
        'check': 'https://agents.ganamos.bet/api/user/check',
        'users': 'https://agents.ganamos.bet/api/agent_admin/user/'
    }
    
    # Headers comunes
    BASE_HEADERS = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "es-419,es;q=0.9,en;q=0.8,pt;q=0.7,it;q=0.6",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "referer": "https://agents.ganamos.bet/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin"
    }
    
    for attempt in range(1, max_retries + 1):
        try:
            # 1. Realizar login
            login_response = requests.post(
                URLS['login'],
                json=CREDENTIALS,
                headers={**BASE_HEADERS, "content-type": "application/json;charset=UTF-8"}
            )
            
            if login_response.status_code != 200:
                raise ValueError(f"Login falló con código {login_response.status_code}")
                
            session_id = login_response.cookies.get("session")
            if not session_id:
                raise ValueError("No se recibió session_id en la respuesta")
            
            # 2. Verificar sesión y obtener parent_id
            check_response = requests.get(
                URLS['check'],
                headers={**BASE_HEADERS, "cookie": f"session={session_id}"}
            )
            
            if check_response.status_code != 200:
                raise ValueError("Error en verificación de usuario")
                
            parent_id = check_response.json()['result']['id']
            
            # 3. Obtener lista de usuarios
            users_response = requests.get(
                URLS['users'],
                params={
                    'count': '1000',  # Número alto para obtener todos los usuarios
                    'page': '0',
                    'user_id': parent_id,
                    'is_banned': 'false',
                    'is_direct_structure': 'false'
                },
                headers={**BASE_HEADERS, "cookie": f"session={session_id}"}
            )
            
            if users_response.status_code != 200:
                raise ValueError("Error obteniendo lista de usuarios")
                
            users_data = users_response.json()
            lista_usuarios = {
                user['username']: user['id'] 
                for user in users_data["result"]["users"]
            }
            
            return lista_usuarios, session_id
            
        except Exception as e:
            if attempt == max_retries:
                raise Exception(f"Fallo después de {max_retries} intentos: {str(e)}")
            time.sleep(retry_delay)

def carga_ganamos(alias: str, monto: float, max_retries: int = 2) -> Tuple[bool, float]:
    """
    Función mejorada para cargar saldo con manejo robusto de errores
    
    Args:
        alias: Nombre de usuario a cargar
        monto: Monto a cargar
        max_retries: Intentos máximos si falla la autenticación
        
    Returns:
        Tuple con (éxito: bool, balance_actual: float)
    """
    # URLs del API
    URLS = {
        'payment': 'https://agents.ganamos.bet/api/agent_admin/user/{}/payment/',
        'balance': 'https://agents.ganamos.bet/api/user/balance'
    }
    
    # Headers comunes
    BASE_HEADERS = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "es-419,es;q=0.9,en;q=0.8,pt;q=0.7,it;q=0.6",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "referer": "https://agents.ganamos.bet/",
        "content-type": "application/json"
    }
    
    for attempt in range(1, max_retries + 1):
        try:
            # Obtener credenciales frescas
            usuarios, session_id = login_ganamos()
            
            if alias not in usuarios:
                raise ValueError(f"Usuario {alias} no encontrado")
                
            id_usuario = usuarios[alias]
            payment_url = URLS['payment'].format(id_usuario)
            
            # Configurar headers con la sesión
            headers = {
                **BASE_HEADERS,
                "cookie": f"session={session_id}"
            }
            
            # Realizar la carga
            payload = {"operation": 0, "amount": float(monto)}
            response = requests.post(
                payment_url,
                json=payload,
                headers=headers
            )
            
            # Si hay error de autenticación, reintentar con nueva sesión
            if response.status_code == 401 and attempt < max_retries:
                continue
                
            if response.status_code != 200:
                error_msg = response.json().get('error_message', 'Error desconocido')
                raise ValueError(f"Error en carga: {error_msg}")
            
            # Obtener balance actual
            balance_response = requests.get(
                URLS['balance'],
                headers=headers
            )
            
            balance = balance_response.json()['result']['balance'] if balance_response.status_code == 200 else 0.0
            
            return True, balance
            
        except Exception as e:
            if attempt == max_retries:
                return False, 0.0
            time.sleep(2)  # Pequeña espera antes de reintentar

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


