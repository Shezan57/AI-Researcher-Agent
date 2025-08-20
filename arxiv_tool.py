# step1: Access arXiv using URL
import requests
import xml.etree.ElementTree as ET
from langchain_core.tools import tool




max_results = 1
topic = "Prompt Engineering"
def search_arxiv_paper(topic: str, max_results: int =5) -> dict:
    query = "+".join(topic.lower().split())
    for char in list('()" '):
        if char in query:
            print(f"invalid character '{char}' in query: {query}")
            raise ValueError(f"Invalid character '{char}' in query: {query}")
    url = (
        "https://export.arxiv.org/api/query?"
        f"search_query=all:{query}"
        f"&max_results={max_results}"
        "&sortBy=submittedDate"
        "&sortOrder=descending"
    )
    print("Requesting URL:", url)
    response = requests.get(url)
    if not response.ok:
        print("ArXiv API Error:", response.status_code)
        raise ValueError(f"Bad response from arXiv API: {response.status_code}\n{response.text}")
    
    data = parse_arxiv_xml(response.text)
    return data  # Return parsed XML data


# step2: Parse XML

def parse_arxiv_xml(xml_string: str) -> dict:
    """Parse the XML string from arXiv API and extract relevant data."""
    entries = []
    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "arxiv": "http://arxiv.org/schemas/atom"
    }
    root = ET.fromstring(xml_string)
    #Loop through each <entry> in Atom namespace
    for entry in root.findall("atom:entry", ns):
        # Extract authors
        authors = [
            author.findtext("atom:name", namespaces=ns)
            for author in entry.findall("atom:author", ns)
        ]
    
        # Extract catagories (term attributes)
        categories = [
            cat.attrib.get("term")
            for cat in entry.findall("atom:category", ns)
        ]
        
        # Extract PDF link (rel="related" and type="application/pdf")
        pdf_link = None
        for link in entry.findall("atom:link", ns):
            if link.attrib.get("type") == "application/pdf":
                pdf_link = link.attrib.get("href")
                break
        
        entries.append({
            "title": entry.findtext("atom:title", namespaces=ns),
            "summary": entry.findtext("atom:summary", namespaces=ns).strip(),
            "authors": authors,
            "categories": categories,
            "pdf_link": pdf_link
        })
    return {"entries": entries}


# print(search_arxiv_paper(topic="prompt engineering",max_results=5))



# step3: Convert the functionality into a tool
@tool
def arxiv_search(topic: str) -> list[dict]:
    """Search for recently uploaded arXiv papaers
    
    Args:
        topic (str): The topic to search for in arXiv.
    Returns:
        list[dict]: A list of dictionaries containing information including title, authors, summary, etc about the found papers.
    """
    print("ARXIV Agent called")
    print(f"Searching arXiv for papers about {topic}")
    papers = search_arxiv_paper(topic)
    if len(papers) == 0:
        print(f"No papers found for topic: {topic}")
        raise ValueError(f"No papers found for topic: {topic}")
    print(f"Found {len(papers['entries'])} papers for topic: {topic}")
    return papers