#!/usr/bin/env python3
"""Academic Search CLI - unified interface to free-tier academic APIs.

Usage:
    python academic_search.py papers "solid state battery" --limit 5
    python academic_search.py citation "10.1038/s41586-021-03819-2"
    python academic_search.py biomedical "mRNA vaccine cancer"
    python academic_search.py preprint "mixture of experts LLM"
    python academic_search.py dataset "climate temperature"
"""

import argparse
import io
import json
import os
import ssl
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Optional

# Force UTF-8 output on Windows
if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding != "utf-8":
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# Create unverified SSL context for environments with cert issues
SSL_CONTEXT = ssl.create_default_context()
SSL_CONTEXT.check_hostname = False
SSL_CONTEXT.verify_mode = ssl.CERT_NONE

# Load API keys from .env file
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
for env_path in [os.path.join(SCRIPT_DIR, ".env"), os.path.join(SKILL_DIR, ".env")]:
    if os.path.isfile(env_path):
        with open(env_path, "r", encoding="utf-8-sig") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key and value and key not in os.environ:
                    os.environ[key] = value

S2_API_KEY = os.environ.get("SEMANTIC_SCHOLAR_API_KEY", "")
METASO_API_KEY = os.environ.get("METASO_API_KEY", "")


def fetch_json(url: str, timeout: int = 15, headers: Optional[dict] = None) -> dict:
    """Fetch URL and parse JSON response."""
    req_headers = {"User-Agent": "AcademicSearch/2.0"}
    if headers:
        req_headers.update(headers)
    req = urllib.request.Request(url, headers=req_headers)
    with urllib.request.urlopen(req, timeout=timeout, context=SSL_CONTEXT) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_xml(url: str, timeout: int = 15) -> str:
    """Fetch URL and return raw text (for XML)."""
    req = urllib.request.Request(url, headers={"User-Agent": "AcademicSearch/2.0"})
    with urllib.request.urlopen(req, timeout=timeout, context=SSL_CONTEXT) as resp:
        return resp.read().decode("utf-8")


# ─── Search Functions ───────────────────────────────────────────

def search_semantic_scholar(query: str, limit: int = 10) -> list[dict]:
    """Search papers via Semantic Scholar API."""
    params = urllib.parse.urlencode({
        "query": query,
        "limit": limit,
        "fields": "title,authors,year,citationCount,journal,externalIds"
    })
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?{params}"
    headers = {}
    if S2_API_KEY:
        headers["x-api-key"] = S2_API_KEY
    data = fetch_json(url, headers=headers)
    results = []
    for paper in data.get("data", []):
        authors = ", ".join(a.get("name", "") for a in paper.get("authors", [])[:3])
        if len(paper.get("authors", [])) > 3:
            authors += " et al."
        results.append({
            "title": paper.get("title", "N/A"),
            "authors": authors,
            "year": paper.get("year", "N/A"),
            "citations": paper.get("citationCount", 0),
            "journal": paper.get("journal", {}).get("name", "") if paper.get("journal") else "",
            "doi": paper.get("externalIds", {}).get("DOI", ""),
        })
    return results


def search_crossref(query: str, limit: int = 10) -> list[dict]:
    """Search papers via Crossref API (free, no key required)."""
    # If input looks like a DOI, do direct DOI lookup
    doi_pattern = r"10\.\d{4,}/[^\s]+"
    import re
    if re.match(doi_pattern, query):
        url = f"https://api.crossref.org/works/{query}"
        data = fetch_json(url)
        msg = data.get("message", {})
        authors = ", ".join(
            f"{a.get('given', '')} {a.get('family', '')}".strip()
            for a in msg.get("author", [])[:3]
        )
        title = msg.get("title", ["N/A"])[0] if msg.get("title") else "N/A"
        return [{
            "title": title,
            "authors": authors,
            "year": msg.get("published-print", {}).get("date-parts", [[0]])[0][0],
            "journal": msg.get("container-title", [""])[0] if msg.get("container-title") else "",
            "doi": msg.get("DOI", query),
            "references_count": msg.get("references-count", 0),
            "cited_by": msg.get("is-referenced-by-count", 0),
        }]

    # Keyword search
    params = urllib.parse.urlencode({
        "query": query,
        "rows": limit,
        "filter": "type:journal-article",
    })
    url = f"https://api.crossref.org/works?{params}"
    data = fetch_json(url)
    results = []
    for item in data.get("message", {}).get("items", []):
        title = item.get("title", ["N/A"])[0] if item.get("title") else "N/A"
        authors = ", ".join(
            f"{a.get('given', '')} {a.get('family', '')}".strip()
            for a in item.get("author", [])[:3]
        )
        results.append({
            "title": title,
            "authors": authors,
            "year": item.get("published-print", {}).get("date-parts", [[0]])[0][0],
            "journal": item.get("container-title", [""])[0] if item.get("container-title") else "",
            "doi": item.get("DOI", ""),
        })
    return results


def search_pubmed(query: str, limit: int = 10) -> list[dict]:
    """Search biomedical literature via PubMed (free, 3req/s)."""
    # Step 1: Search for IDs
    params = urllib.parse.urlencode({
        "db": "pubmed",
        "term": query,
        "retmax": limit,
        "retmode": "json",
    })
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?{params}"
    data = fetch_json(url)
    ids = data.get("esearchresult", {}).get("idlist", [])
    if not ids:
        return []

    # Step 2: Fetch summaries
    summary_url = (
        f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
        f"?db=pubmed&id={','.join(ids)}&retmode=json"
    )
    summary = fetch_json(summary_url)

    results = []
    for pid in ids:
        rec = summary.get("result", {}).get(pid, {})
        authors_list = []
        for au in rec.get("authors", [])[:3]:
            authors_list.append(au.get("name", ""))
        authors = ", ".join(authors_list)
        if len(rec.get("authors", [])) > 3:
            authors += " et al."

        results.append({
            "title": rec.get("title", "N/A"),
            "authors": authors,
            "year": rec.get("pubdate", "")[:4] if rec.get("pubdate") else "N/A",
            "journal": rec.get("source", ""),
            "pmid": pid,
            "doi": next(
                (a.get("value", "") for a in rec.get("articleids", [])
                 if a.get("idtype") == "doi"), ""
            ),
        })
    return results


def search_arxiv(query: str, limit: int = 10) -> list[dict]:
    """Search preprints via arXiv API (free, no key required)."""
    params = urllib.parse.urlencode({
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": limit,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    })
    url = f"http://export.arxiv.org/api/query?{params}"
    xml_text = fetch_xml(url)

    # Parse Atom XML
    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "arxiv": "http://arxiv.org/schemas/atom",
    }
    root = ET.fromstring(xml_text)
    results = []
    for entry in root.findall("atom:entry", ns):
        title = entry.find("atom:title", ns)
        title_text = title.text.strip() if title is not None else "N/A"

        authors_list = []
        for au in entry.findall("atom:author", ns)[:3]:
            name = au.find("atom:name", ns)
            if name is not None:
                authors_list.append(name.text.strip())
        authors = ", ".join(authors_list)

        published = entry.find("atom:published", ns)
        year = published.text[:4] if published is not None and published.text else "N/A"

        arxiv_id = entry.find("atom:id", ns)
        arxiv_id_text = arxiv_id.text.strip().split("/abs/")[-1] if arxiv_id is not None else ""

        results.append({
            "title": title_text,
            "authors": authors,
            "year": year,
            "journal": f"arXiv:{arxiv_id_text}",
            "arxiv_id": arxiv_id_text,
        })
    return results


def search_zenodo(query: str, limit: int = 10) -> list[dict]:
    """Search research datasets via Zenodo API (free, no key required)."""
    params = urllib.parse.urlencode({
        "q": query,
        "size": limit,
        "sort": "mostrecent",
    })
    url = f"https://zenodo.org/api/records?{params}"
    data = fetch_json(url)
    results = []
    for hit in data.get("hits", {}).get("hits", []):
        meta = hit.get("metadata", {})
        authors = ", ".join(
            c.get("name", "") for c in meta.get("creators", [])[:3]
        )
        results.append({
            "title": meta.get("title", "N/A"),
            "authors": authors,
            "year": meta.get("publication_date", "")[:4],
            "doi": meta.get("doi", ""),
            "type": meta.get("resource_type", {}).get("title", ""),
        })
    return results


def search_metaso(query: str, limit: int = 10) -> list[dict]:
    """Search via Metaso (秘塔搜索) - Chinese academic/tech search."""
    if not METASO_API_KEY:
        raise RuntimeError("METASO_API_KEY not set. Add it to .env file.")
    url = "https://metaso.cn/api/v1/search"
    payload = json.dumps({"q": query, "n": limit}).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {METASO_API_KEY}",
        "Content-Type": "application/json",
    }
    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=20, context=SSL_CONTEXT) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    results = []
    for page in data.get("webpages", []):
        results.append({
            "title": page.get("title", "N/A"),
            "url": page.get("link", page.get("url", "")),
            "snippet": page.get("snippet", ""),
            "date": page.get("date", ""),
            "authors": page.get("authors", ""),
        })
    return results


# ─── Output ─────────────────────────────────────────────────────

SOURCES = {
    "papers": search_semantic_scholar,
    "citation": search_crossref,
    "biomedical": search_pubmed,
    "preprint": search_arxiv,
    "dataset": search_zenodo,
    "metaso": search_metaso,
}


def format_results(source: str, results: list[dict]) -> str:
    """Format results as Markdown."""
    lines = [f"## {source.upper()} 搜索结果 ({len(results)} 条)\n"]
    for i, r in enumerate(results, 1):
        lines.append(f"### {i}. {r.get('title', 'N/A')}")
        if r.get("authors"):
            lines.append(f"- 作者: {r['authors']}")
        if r.get("journal"):
            lines.append(f"- 来源: {r['journal']} ({r.get('year', '')})")
        elif r.get("year"):
            lines.append(f"- 年份: {r['year']}")
        if r.get("doi"):
            lines.append(f"- DOI: [{r['doi']}](https://doi.org/{r['doi']})")
        if r.get("pmid"):
            lines.append(f"- PMID: {r['pmid']} ([PubMed](https://pubmed.ncbi.nlm.nih.gov/{r['pmid']}))")
        if "citations" in r:
            lines.append(f"- 引用次数: {r['citations']}")
        if "cited_by" in r:
            lines.append(f"- 被引次数: {r['cited_by']}")
        if r.get("arxiv_id"):
            lines.append(f"- arXiv: [{r['arxiv_id']}](https://arxiv.org/abs/{r['arxiv_id']})")
        if r.get("type"):
            lines.append(f"- 类型: {r['type']}")
        if r.get("url"):
            lines.append(f"- 链接: {r['url']}")
        if r.get("snippet"):
            lines.append(f"- 摘要: {r['snippet'][:200]}...")
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Academic Search CLI - 直连学术 API 免费层",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
数据源:
  papers      Semantic Scholar (2亿+论文)  [100req/5min]
  citation    Crossref (DOI查询/引用关系)   [无限]
  biomedical  PubMed (生物医学文献)         [3req/s]
  preprint    arXiv (预印本)               [无限]
  dataset     Zenodo (研究数据集)           [无限]
  metaso      秘塔搜索 (中文学术/技术)       [需API Key]

示例:
  python academic_search.py papers "solid state battery" --limit 5
  python academic_search.py citation "10.1038/s41586-021-03819-2"
  python academic_search.py biomedical "mRNA vaccine cancer"
  python academic_search.py preprint "large language model reasoning"
  python academic_search.py dataset "global temperature"
  python academic_search.py metaso "固态电池 最新进展" --limit 5
        """,
    )
    parser.add_argument("source", choices=list(SOURCES.keys()),
                        help="数据源")
    parser.add_argument("query", help="搜索关键词或 DOI")
    parser.add_argument("--limit", "-n", type=int, default=10,
                        help="返回数量 (默认10)")
    parser.add_argument("--json", action="store_true",
                        help="输出原始 JSON")
    args = parser.parse_args()

    try:
        results = SOURCES[args.source](args.query, args.limit)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(format_results(args.source, results))


if __name__ == "__main__":
    main()
