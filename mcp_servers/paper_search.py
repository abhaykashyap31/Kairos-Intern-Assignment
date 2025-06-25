import requests
import xml.etree.ElementTree as ET

def paper_search(query: str, max_results: int):
    """Queries the arXiv API and returns up to max_results items."""
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={max_results}"
    response = requests.get(url)
    if response.status_code != 200:
        return [f"arXiv API error: {response.status_code}"]
    root = ET.fromstring(response.text)
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    results = []
    for entry in root.findall('atom:entry', ns):
        title = entry.find('atom:title', ns).text.strip()
        authors = [a.find('atom:name', ns).text for a in entry.findall('atom:author', ns)]
        summary = entry.find('atom:summary', ns).text.strip()
        link = entry.find('atom:id', ns).text.strip()
        results.append({
            'title': title,
            'authors': authors,
            'summary': summary,
            'link': link
        })
    return results 