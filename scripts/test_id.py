from academic_search import search_arxiv
r = search_arxiv('transformer', 2)
for x in r:
    print('id:', repr(x.get('arxiv_id','MISSING')))
