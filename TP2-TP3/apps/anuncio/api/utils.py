import requests
from django.core.cache import cache

def cotizar_usd():
    
    tasa_usd = cache.get('tasa_ars_a_usd')
    
    if tasa_usd is None:
        try:
            url = 'https://open.er-api.com/v6/latest/ARS'
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                tasa_usd = data['rates'].get('USD')
                if tasa_usd:
                    cache.set('tasa_ars_a_usd', tasa_usd, 3600)
        except requests.exceptions.RequestException:
            return None
            
    return tasa_usd