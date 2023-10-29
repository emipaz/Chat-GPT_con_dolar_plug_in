from requests import get
import os
import openai
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key = os.environ['OPENAI_API_KEY']


def consulta_con_funcion(messages):
    """
    Realiza una consulta utilizando la función de OpenAI ChatCompletion con funciones
    como plug_in
    
    Parámetros:
    - messages: Una lista de mensajes que se utilizarán como contexto para la consulta.

    Retorna:
    - El resultado de la consulta utilizando la función de OpenAI ChatCompletion.

    """
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        max_tokens=250,
        functions=funciones,
        function_call="auto"
    )
    
def consulta(messages):
    """
    Realiza una consulta utilizando la función de OpenAI ChatCompletion.

    Parámetros:
    - messages: Una lista de mensajes que se utilizarán como contexto para la consulta.

    Retorna:
    - El resultado de la consulta utilizando la función de OpenAI ChatCompletion.
    """
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        max_tokens=250,
    )
     

def rol_content_func(response):
    """
    Extrae información relevante de la respuesta proporcionada por Chat-GPT

    Parámetros:
    - response: La respuesta obtenida de OpenAI ChatCompletion.

    Retorna:
    - Una tupla con el rol, el contenido y los datos de la función (si están presentes) de la respuesta.

    """
    response_dict = response.choices[0].to_dict()
    rol = response_dict["message"]["role"]
    content = response_dict["message"]["content"]
    hay_funcion = response_dict["message"].get("function_call", False)
    if hay_funcion:
        funcion = response_dict["message"]["function_call"]["name"]
        argumentos = response_dict["message"]["function_call"]["arguments"]
        datos_funcion = (funcion, argumentos)
    else:
        datos_funcion = False
    return rol, content, datos_funcion

# funcion para consultar el dolar como plug_in
# consulta la api dolarapi.com

def consulta_dolar():
    """Consulta las cotizaciones del dolar en argentina"""
    dolar = get("https://dolarapi.com/v1/dolares")
    if dolar.status_code == 200:
        dolar = dolar.json()
    else:
        return "Error al consultar la API"
    return str(dolar)

# lista de funciones disponibles para el plug_in

funciones = [
            {
                "name": "consulta_dolar",
                "description": "Consulta las cotizaciones del dolar en argentina",
                "parameters": {
                                "type": "object",
                                "properties": {}
                                },
                "required": [],
            },
            ]
