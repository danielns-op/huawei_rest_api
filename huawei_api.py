#!/usr/bin/python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------- #
# Autor: Daniel Noronha da Silva                                      #
#  Data: 03/11/2022                                                   #
# ------------------------------------------------------------------- #
# Descrição:                                                          #
#   This library was created for easily the conexion and the get data #
#   with REST API from OceanStor Dorado 6.1.0.                        #
# ------------------------------------------------------------------- #

# - Imports --------------------------------------------------------- #
import requests
import ssl
import urllib3
# ------------------------------------------------------------------- #

# Iguinorar o alerta de certificado
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ssl.CERT_REQUIRED = None
# ------------------------------------------------------------------- #

# - Funções --------------------------------------------------------- #

class STGHuawei:
  def __init__(self, ip, port, user, pwd):
    self.ip = ip
    self.port = port
    self.user = user
    self.pwd = pwd
    self.session = requests.Session()
    self.headers = requests.utils.default_headers()

  def generate_token(self):
    """
    Generates token and get device ID from Huawei API. This token is used for get
    information from storage.

    Returns:
        dict: A dictionary containing a key called data, this key is a list of
        data from storage.
    """
    url = f"https://{self.ip}:{self.port}/deviceManager/rest/xxx/sessions"

    body = {
      "username": self.user,
      "password": self.pwd,
      "scope": "0"
    }

    response = self.session.post(url=url, json=body, verify=False)
    dados = response.json()

    try:
      device_id = dados["data"]["deviceid"]
      token = dados["data"]["iBaseToken"]
      print("Token gerado com sucesso!")
      return device_id, token
    except Exception:
      print(f"Falha ao obter o TOKEN\n{dados}")
      exit(1)

  def query_storagepool_info(self, device_id, headers):
    """
      This interface is used to batch query basic information about storage pools.

    Args:
        device_id (string): Storage pool ID.
        headers (Object): Object from requests structure that was instantiated on
                          the property self.headers from STGHuawei class.
    Returns:
        JSON Response Content: A JSON containing the storage pool data.
    """
    url = f"https://{self.ip}:{self.port}/deviceManager/rest/{device_id}/storagepool"
    response = self.session.get(url=url, headers=headers, verify=False)
    return response.json()


# ------------------------------------------------------------------- #
