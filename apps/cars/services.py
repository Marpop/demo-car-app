import logging

from django.conf import settings

import requests

logger = logging.getLogger(__name__)


def _call_api(endpoint):
    try:
        response = requests.get(f"{endpoint}?format=json")
        if response.status_code != 200:
            logger.error(response.text)
            return None
        return response.json().get("Results")
    except requests.exception.RequestException as error:
        logger.exception(error)
        raise SystemExit(error)



def get_all_makes():
    endpoint = settings.VEHIDLE_GET_ALL_MAKES
    return _call_api(endpoint)


def get_models_for_make(make: str):
    endpoit = settings.VEHICLE_GET_MODELS_BY_MAKE
    return _call_api(f"{endpoit}/{make}")
