from fastapi import HTTPException
from pydantic import BaseModel
import os
import requests
from urllib.parse import quote_plus, unquote

class Service(BaseModel):
    service: str
    query: str 

def get_service(request: Service):
    if request.service == 'zendesk':
        baseUrl = os.getenv("ZENDESK_URL")
        # Decodifique a consulta se ela já estiver codificada
        decoded_query = unquote(request.query)

        # Verifica se a query já está codificada
        if decoded_query != request.query:
        # Caso já esteja codificada, usamos diretamente a versão passada
            normalized_query = request.query
        else:
        # Caso não esteja codificada, normalizamos a consulta
            normalized_query = quote_plus(decoded_query)

        full_url = baseUrl + request.query
        
        try:
            response = requests.get(full_url)
            ##response.raise_for_status()  # Verifica se houve algum erro na requisição
            
            return response.json()  # Retorna o resultado da requisição como JSON
        except requests.exceptions.HTTPError as http_err:
            raise HTTPException(status_code=response.status_code, detail='QUERY: ' + request.query)
        except Exception as err:
            raise HTTPException(status_code=500, detail='QUERY: ' + request.query)
    else:
        raise HTTPException(status_code=400, detail="Serviço não suportado.")
