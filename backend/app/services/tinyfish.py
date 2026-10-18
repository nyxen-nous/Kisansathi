"""Server-side TinyFish transport. No keys or raw upstream errors reach clients."""
import httpx
from .. import config

class TinyFishError(Exception):
    def __init__(self, code):
        self.code = code
        super().__init__(code)

async def _request(method, url, **kwargs):
    if not config.TINYFISH_API_KEY:
        raise TinyFishError('schemes_not_configured')
    try:
        async with httpx.AsyncClient(timeout=config.TINYFISH_TIMEOUT_SECONDS, follow_redirects=False) as client:
            response = await client.request(method, url, headers={'X-API-Key': config.TINYFISH_API_KEY}, **kwargs)
            if response.status_code == 429:
                raise TinyFishError('schemes_busy')
            response.raise_for_status()
            payload = response.json()
            if not isinstance(payload, dict) or not isinstance(payload.get('results'), list):
                raise ValueError('Invalid payload')
            return payload
    except (httpx.HTTPError, ValueError):
        raise TinyFishError('schemes_unavailable') from None

async def search(query):
    return await _request('GET', 'https://api.search.tinyfish.ai', params={
        'query': query, 'location': 'IN', 'language': 'en',
        'include_domains': 'gov.in,nic.in',
        'purpose': 'Find official farmer assistance schemes. State applicability and current application status must be checked from the source.'})

async def fetch(urls):
    return await _request('POST', 'https://api.fetch.tinyfish.ai', json={
        'urls': urls, 'format': 'markdown', 'ttl': 0,
        'purpose': 'Read scheme benefits, eligibility, documents, application process and scheme period exactly as published.'})
