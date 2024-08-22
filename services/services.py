from fastapi import HTTPException
from pydantic import BaseModel
import os
import requests
from urllib.parse import quote_plus

class Service(BaseModel):
    service: str
    query: str  # Adicionei um campo para a consulta

def get_service(request: Service):
    if request.service == 'zendesk':
        baseUrl = os.getenv("ZENDESK_URL")
        normalized_query = quote_plus(request.query, safe='')
        full_url = baseUrl + normalized_query

        #Debug
        print('QUERY: ' + request.query)
        
        try:
            response = requests.get(full_url)
            response.raise_for_status()  # Verifica se houve algum erro na requisição
            
            return response.json()  # Retorna o resultado da requisição como JSON
        except requests.exceptions.HTTPError as http_err:
            raise HTTPException(status_code=response.status_code, detail=str(http_err))
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))
    else:
        raise HTTPException(status_code=400, detail="Serviço não suportado.")
