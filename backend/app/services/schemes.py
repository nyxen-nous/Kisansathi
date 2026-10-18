"""Live official-source discovery; excerpts are not eligibility determinations."""
import re
from datetime import datetime, timezone, date
from urllib.parse import urlsplit
from . import tinyfish

CATEGORIES = {
    'irrigation': 'farmer irrigation drip sprinkler assistance subsidy scheme',
    'solar': 'farmer solar pump PM KUSUM assistance scheme',
    'equipment': 'farmer agricultural machinery equipment assistance scheme',
    'insurance': 'farmer crop insurance scheme',
    'income': 'farmer income support assistance scheme',
}
SEEDS = {'solar': [('PM-KUSUM — Ministry of New and Renewable Energy',
    'https://mnre.gov.in/en/pradhan-mantri-kisan-urja-suraksha-evam-utthaan-mahabhiyaan-pm-kusum/')]}

def official_url(url):
    try:
        p = urlsplit(url)
        h = (p.hostname or '').lower()
        return p.scheme == 'https' and not p.username and not p.password and p.port in (None, 443) and (h.endswith('.gov.in') or h.endswith('.nic.in'))
    except (ValueError, TypeError):
        return False

def extract_sections(text):
    patterns = {
        'benefits': r'benefit|assistance|subsid|salient features|financial support',
        'eligibility': r'eligib|who can apply',
        'documents': r'documents required|required documents',
        'application': r'application process|how to apply|whom to contact',
        'period': r'^(?:scheme )?period$|deadline|last date|duration',
    }
    sections = {key: [] for key in patterns}
    active = None
    for raw in text[:120000].splitlines():
        line = raw.strip()
        heading = line.lstrip('#').strip().strip('*').strip(':').strip()
        is_heading = line.startswith('#') or (len(heading) < 90 and line.startswith('**') and line.endswith('**'))
        if is_heading:
            active = next((key for key, pattern in patterns.items() if re.search(pattern, heading, re.I)), None)
        elif line and active and sum(map(len, sections[active])) < 2400:
            sections[active].append(line[:900])
    return {k: '\n'.join(v)[:2400] or None for k,v in sections.items()}

def past_period(period):
    for d,m,y in re.findall(r'\b(\d{1,2})[./-](\d{1,2})[./-](20\d{2})\b', period or ''):
        try:
            if date(int(y),int(m),int(d)) < datetime.now(timezone.utc).date(): return True
        except ValueError: pass
    return False

async def discover(state, category):
    query = f'{state} {CATEGORIES[category]} benefits eligibility application official'
    found = await tinyfish.search(query)
    candidates = []
    seen = set()
    for title, url in SEEDS.get(category, []):
        candidates.append({'title': title, 'url': url}); seen.add(url)
    for result in found['results']:
        if not isinstance(result, dict): continue
        url = result.get('url', '')
        if official_url(url) and url not in seen:
            candidates.append({'title': str(result.get('title') or 'Official source')[:240], 'url': url})
            seen.add(url)
        if len(candidates) >= 5: break
    stamp = datetime.now(timezone.utc).isoformat()
    if not candidates:
        return {'results': [], 'retrieved_at': stamp, 'query': query, 'provider': 'TinyFish Search + Fetch', 'partial': False}
    fetched = await tinyfish.fetch([c['url'] for c in candidates])
    pages = {p.get('url'): p for p in fetched['results'] if isinstance(p,dict)}
    results = []
    for c in candidates:
        page = pages.get(c['url'], {})
        text = page.get('text', '')
        if not isinstance(text, str): text = ''
        final_url = page.get('final_url') or c['url']
        readable = official_url(final_url) and len(text.strip()) >= 350 and bool(re.search(r'farmer|agricultur|irrigation|किसान', text, re.I))
        sections = extract_sections(text) if readable else {}
        results.append({**c, 'url': final_url if official_url(final_url) else c['url'],
            'status': 'extracted' if readable else 'details_unavailable',
            'sections': sections,
            'excerpt': text[:1500] if readable else None,
            'state_mentioned': bool(readable and state.casefold() in text.casefold()),
            'past_period': past_period(sections.get('period')),
            'published_date': page.get('published_date') if readable else None,
            'retrieved_at': stamp})
    return {'results': results, 'retrieved_at': stamp, 'query': query,
            'provider': 'TinyFish Search + Fetch', 'partial': any(r['status'] != 'extracted' for r in results)}
