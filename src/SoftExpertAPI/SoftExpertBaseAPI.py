import base64
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, Optional

import requests
from requests import Response




from .SoftExpertOptions import SoftExpertOptions
from .SoftExpertException import SoftExpertException

class SoftExpertBaseAPI:
    """
    Base class for all SoftExpert API classes.

    It provides basic methods for making HTTP requests and parsing responses.
    """

    def __init__(self, options: SoftExpertOptions, endpoint: str):
        """
        Constructor.

        :param options: SoftExpertOptions.
        """
        self._url = options.url
        self._userID = options.userID
        self._authorization = options.authorization
        self._endpoint = endpoint # cada subclasse deve definir o endpoint




    def request(self, action: str, xml_body: str) -> requests.Response:
        headers = {
            'Content-Type': 'text/xml;charset=UTF-8',
            'Authorization': self._authorization,
            'SOAPAction': action
        }

        #try:
        response = requests.post(self._url+self._endpoint, data=xml_body, headers=headers, verify=False)
        body = response.text

        if response.status_code == 502:
            raise SoftExpertException.SoftExpertException(f"Provavel que o SoftExpert esteja fora do ar. {body}")
        
        if response.status_code == 401:
            raise SoftExpertException.SoftExpertException(f"Cheque se a sua autenticação está correta. {body}")
        
        if response.status_code != 200:
            raise SoftExpertException.SoftExpertException(f"{body}")

        return body

        #except Exception as e:
        #    raise Exception(f"Não foi possível estabelecer uma conexão com o SoftExpert. Reveja sua URL e sua rede. Details: {e}")
        
        

    def _remove_namespace(xml):
        return xml.replace('xmlns="urn:workflow"', '')
