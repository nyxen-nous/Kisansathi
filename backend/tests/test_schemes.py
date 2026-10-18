import asyncio
import httpx
import pytest
from app import config
from app.services import schemes, tinyfish

@pytest.mark.parametrize('url,expected',[
 ('https://mnre.gov.in/scheme',True),('https://x.nic.in/scheme',True),
 ('https://mnre.gov.in.evil.com',False),('https://evilgov.in',False),
 ('http://mnre.gov.in',False),('https://user@mnre.gov.in',False),
 ('http://127.0.0.1',False),('https://mnre.gov.in:9999',False)])
def test_official_source_boundary(url,expected):
    assert schemes.official_url(url) is expected

def test_period_and_sections():
    s=schemes.extract_sections('## Period\nTill 31.03.2026\n## Eligibility\nIndividual farmers.\n## Relevant Documents\nNot an applicant checklist.')
    assert schemes.past_period(s['period'])
    assert s['eligibility']=='Individual farmers.'
    assert s['documents'] is None

def test_partial_pages(client,monkeypatch):
    async def search(query):
        return {'results':[{'url':'https://example.gov.in/farm','title':'Farm assistance'}, {'url':'https://example.nic.in/empty','title':'Empty'}, {'url':'https://evil.com','title':'Reject'}]}
    async def fetch(urls):
        assert len(urls)==2
        return {'results':[{'url':urls[0],'text':'## Benefits\n'+'Farmers receive assistance. '*25+'\n## Period\nTill 31.03.2026'}, {'url':urls[1],'text':'Copyright footer'}]}
    monkeypatch.setattr(tinyfish,'search',search);monkeypatch.setattr(tinyfish,'fetch',fetch)
    r=client.post('/api/schemes/search',json={'state':'Punjab','category':'irrigation'})
    assert r.status_code==200
    data=r.json();assert data['partial']
    assert data['results'][0]['past_period']
    assert not data['results'][0]['state_mentioned']
    assert data['results'][1]['status']=='details_unavailable'
    assert data['results'][1]['excerpt'] is None

def test_missing_key_and_validation(client,monkeypatch):
    monkeypatch.setattr(config,'TINYFISH_API_KEY','')
    r=client.post('/api/schemes/search',json={'state':'Punjab','category':'solar'})
    assert r.status_code==503 and r.json()['detail']=='schemes_not_configured'
    assert client.post('/api/schemes/search',json={'state':'Punjab','category':'bad'}).status_code==422
    assert client.post('/api/schemes/search',json={'state':'Punjab','category':'solar','url':'https://evil.com'}).status_code==422

@pytest.mark.parametrize('status,code',[(401,'schemes_unavailable'),(429,'schemes_busy'),(503,'schemes_unavailable')])
def test_transport_failure_redaction(monkeypatch,status,code):
    real_client=httpx.AsyncClient
    transport=httpx.MockTransport(lambda req:httpx.Response(status,json={'error':'PRIVATE KEY SHOULD NOT LEAK'}))
    monkeypatch.setattr(config,'TINYFISH_API_KEY','secret-test-key')
    monkeypatch.setattr(httpx,'AsyncClient',lambda **kwargs:real_client(transport=transport,**kwargs))
    with pytest.raises(tinyfish.TinyFishError) as error:asyncio.run(tinyfish.search('test'))
    assert str(error.value)==code

def test_transport_contract(monkeypatch):
    requests=[]
    def handle(req):
        requests.append(req)
        assert req.headers['X-API-Key']=='test-key'
        return httpx.Response(200,json={'results':[]})
    real_client=httpx.AsyncClient
    monkeypatch.setattr(config,'TINYFISH_API_KEY','test-key')
    monkeypatch.setattr(httpx,'AsyncClient',lambda **kwargs:real_client(transport=httpx.MockTransport(handle),**kwargs))
    asyncio.run(tinyfish.search('Punjab farm'));asyncio.run(tinyfish.fetch(['https://mnre.gov.in/']))
    assert requests[0].method=='GET' and requests[0].url.host=='api.search.tinyfish.ai'
    assert requests[1].method=='POST' and requests[1].url.host=='api.fetch.tinyfish.ai'

def test_empty_search(client,monkeypatch):
    async def search(query):return {'results':[]}
    monkeypatch.setattr(tinyfish,'search',search)
    assert client.post('/api/schemes/search',json={'state':'Punjab','category':'income'}).json()['results']==[]

def test_readable_redirect_to_untrusted_is_rejected(client,monkeypatch):
    async def search(query):return {'results':[{'url':'https://a.gov.in','title':'A'}]}
    async def fetch(urls):return {'results':[{'url':urls[0],'final_url':'https://evil.com','text':'Farmers '*100}]}
    monkeypatch.setattr(tinyfish,'search',search);monkeypatch.setattr(tinyfish,'fetch',fetch)
    assert client.post('/api/schemes/search',json={'state':'Punjab','category':'income'}).json()['results'][0]['status']=='details_unavailable'

def test_rate_limit(client,monkeypatch):
    async def search(query):return {'results':[]}
    monkeypatch.setattr(tinyfish,'search',search)
    for _ in range(6):assert client.post('/api/schemes/search',json={'state':'Punjab','category':'income'}).status_code==200
    assert client.post('/api/schemes/search',json={'state':'Punjab','category':'income'}).status_code==429
