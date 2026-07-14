# 学术 API 参考

> 本文档列出 academic-search Skill 使用的全部学术 API，包括端点、参数、速率限制和响应格式。

## API 总览

| # | API | 端点 | 免费层 | Key | 用途 |
|---|-----|------|:--:|:--:|------|
| 1 | Semantic Scholar | `api.semanticscholar.org` | 100req/5min | 可选 | 论文语义搜索 |
| 2 | Crossref | `api.crossref.org` | 无限 | 无需 | DOI 元数据 / 引用 |
| 3 | PubMed | `eutils.ncbi.nlm.nih.gov` | 3req/s | 可选 | 生物医学文献 |
| 4 | Europe PMC | `www.ebi.ac.uk/europepmc` | 无限 | 无需 | 生物医学文献（欧洲） |
| 5 | arXiv | `export.arxiv.org` | 无限 | 无需 | 预印本搜索 |
| 6 | Zenodo | `zenodo.org/api` | 无限 | 无需 | 研究数据集 |
| 7 | 秘塔搜索 | `metaso.cn` | 需要 Key | **推荐** | 中文学术/技术实时搜索 |
| 8 | 中文学术站点 | Exa site: 过滤 | **免费** | 无需 | 知网/万方/维普/百度学术 |

---

## 1. Semantic Scholar API

**端点**：`https://api.semanticscholar.org/graph/v1/paper/search`

**速率限制**：
- 无 Key：100 请求 / 5 分钟
- 有 Key：更高限额（[申请](https://www.semanticscholar.org/product/api#api-key-form)）

**搜索论文**：
```
GET https://api.semanticscholar.org/graph/v1/paper/search?query={keywords}&limit={n}&fields=title,authors,year,citationCount,journal,externalIds,abstract
```

**参数**：

| 参数 | 必需 | 说明 | 示例 |
|------|:--:|------|------|
| `query` | ✅ | 搜索关键词（URL 编码） | `solid+state+battery` |
| `limit` | ❌ | 返回数量，默认 10，最大 100 | `5` |
| `offset` | ❌ | 分页偏移 | `10` |
| `fields` | ❌ | 返回字段（逗号分隔） | `title,citationCount,year` |
| `year` | ❌ | 年份过滤 | `2023-2026` |
| `fieldsOfStudy` | ❌ | 学科过滤 | `Computer Science` |

**可用 fields**：
`title`, `abstract`, `authors`, `year`, `citationCount`, `journal`, `externalIds`（DOI）, `publicationTypes`, `openAccessPdf`, `fieldsOfStudy`

**响应格式**：
```json
{
  "total": 12345,
  "data": [
    {
      "paperId": "abc123",
      "title": "Solid-state batteries...",
      "authors": [{"name": "John Doe"}],
      "year": 2024,
      "citationCount": 245,
      "journal": {"name": "Nature Energy"},
      "externalIds": {"DOI": "10.1038/..."}
    }
  ]
}
```

**搜索示例**：
```bash
curl "https://api.semanticscholar.org/graph/v1/paper/search?query=solid+state+battery+electrolyte&limit=5&fields=title,authors,year,citationCount,journal,externalIds"
```

---

## 2. Crossref API

**端点**：`https://api.crossref.org/works/{doi}`

**速率限制**：无硬性限制，礼貌使用即可

**DOI 查询**：
```
GET https://api.crossref.org/works/{doi}
```

**关键词搜索**：
```
GET https://api.crossref.org/works?query={keywords}&rows={n}&filter=type:journal-article
```

**参数**：

| 参数 | 说明 | 示例 |
|------|------|------|
| `query` | 关键词 | `battery+solid+electrolyte` |
| `rows` | 返回数量 | `5` |
| `filter` | 过滤条件 | `type:journal-article,from-pub-date:2023` |
| `sort` | 排序 | `relevance` / `published` |

**响应格式**：
```json
{
  "message": {
    "title": ["Highly Accurate Protein Structure..."],
    "author": [{"given": "John", "family": "Jumper"}],
    "DOI": "10.1038/s41586-021-03819-2",
    "published-print": {"date-parts": [[2021, 7, 15]]},
    "container-title": ["Nature"],
    "reference": [{"DOI": "10.xxx/yyy", ...}, ...],
    "is-referenced-by-count": 25000
  }
}
```

**搜索示例**：
```bash
# DOI 查询
curl "https://api.crossref.org/works/10.1038/s41586-021-03819-2"

# 关键词搜索
curl "https://api.crossref.org/works?query=solid+state+battery&rows=5&filter=type:journal-article"
```

---

## 3. PubMed E-utilities

**端点**：
- 搜索：`https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi`
- 详情：`https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi`

**速率限制**：无 Key 3req/s，有 Key 10req/s

**搜索流程**（两步）：
```
Step 1: esearch → 获取 PMID 列表
Step 2: esummary → 获取论文详情
```

**Step 1 - 搜索**：
```
GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={keywords}&retmax={n}&retmode=json
```

**Step 2 - 详情**：
```
GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={pmid1,pmid2}&retmode=json
```

**搜索示例**：
```bash
# Step 1: 搜索
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=mRNA+vaccine+cancer+immunotherapy&retmax=5&retmode=json"

# Step 2: 获取详情（用 Step 1 返回的 PMID）
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=12345,67890&retmode=json"
```

---

## 4. Europe PMC API

**端点**：`https://www.ebi.ac.uk/europepmc/webservices/rest/search`

**速率限制**：无限制

**搜索**：
```
GET https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={keywords}&resultType=core&pageSize={n}&format=json
```

**参数**：

| 参数 | 说明 | 示例 |
|------|------|------|
| `query` | 关键词（支持 PubMed 语法） | `cancer AND immunotherapy` |
| `resultType` | `core`（摘要+元数据）或 `lite`（仅标题） | `core` |
| `pageSize` | 返回数量，最大 1000 | `10` |
| `format` | `json` 或 `xml` | `json` |

**搜索示例**：
```bash
curl "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=COVID-19+vaccine+efficacy&resultType=core&pageSize=5&format=json"
```

---

## 5. arXiv API

**端点**：`http://export.arxiv.org/api/query`

**速率限制**：无硬性限制，礼貌使用

**搜索**：
```
GET http://export.arxiv.org/api/query?search_query={field}:{keywords}&start={offset}&max_results={n}&sortBy=submittedDate&sortOrder=descending
```

**搜索字段**：
- `all`：所有字段
- `ti`：标题
- `au`：作者
- `abs`：摘要
- `cat`：分类（如 `cs.AI`, `physics`）

**响应格式**：Atom XML

**搜索示例**：
```bash
curl "http://export.arxiv.org/api/query?search_query=all:mixture+of+experts+large+language+model&start=0&max_results=5&sortBy=submittedDate&sortOrder=descending"
```

---

## 6. Zenodo API

**端点**：`https://zenodo.org/api/records`

**速率限制**：无硬性限制

**搜索**：
```
GET https://zenodo.org/api/records?q={keywords}&size={n}&sort=mostrecent
```

**搜索示例**：
```bash
curl "https://zenodo.org/api/records?q=climate+temperature+dataset&size=5&sort=mostrecent"
```

---

## 7. 秘塔搜索 API

**端点**：`POST https://metaso.cn/api/v1/search`

**速率限制**：按 credits 计费

**认证**：需要 API Key（Bearer Token）

**请求格式**：
```
POST https://metaso.cn/api/v1/search
Authorization: Bearer {api_key}
Content-Type: application/json

{"q": "查询关键词", "n": 返回数量}
```

**参数**：

| 参数 | 必需 | 说明 | 示例 |
|------|:--:|------|------|
| `q` | ✅ | 搜索关键词 | `固态电池 最新进展` |
| `n` | ❌ | 返回数量 | `5` |

**响应格式**：
```json
{
  "credits": 3,
  "webpages": [
    {
      "title": "论文/文章标题",
      "link": "https://...",
      "snippet": "内容摘要...",
      "date": "2025年01月01日",
      "authors": "作者名",
      "score": 0.95
    }
  ]
}
```

**特点**：
- 中文内容覆盖极好（学术论文、行业报告、技术博客、B站视频）
- 实时搜索（非静态索引）
- 适合中文技术调研和产业动态追踪

**搜索示例**：
```bash
curl -X POST "https://metaso.cn/api/v1/search" \
  -H "Authorization: Bearer $METASO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q":"固态电池 2025 产业进展","n":5}'
```

---

## 8. 中文学术站点搜索（papers_zh）

**端点**：通过 Exa `websearch_web_search_exa` + site 过滤

**速率限制**：取决于 Exa 免费额度（1,000 次/月）

**认证**：无需额外 Key（使用已有 Exa 工具）

**搜索方式**：
```
websearch_web_search_exa "关键词 site:cnki.net OR site:cqvip.com OR site:wanfangdata.com.cn OR site:xueshu.baidu.com OR site:arxiv.org"
```

**覆盖站点**：

| 站点 | 域名 | 说明 |
|------|------|------|
| 知网 | cnki.net | 中国最大的学术文献数据库 |
| 维普 | cqvip.com | 中文期刊全文数据库 |
| 万方 | wanfangdata.com.cn | 学术期刊/学位论文/会议论文 |
| 百度学术 | xueshu.baidu.com | 中英文学术资源聚合 |
| arXiv | arxiv.org | 预印本（含大量中国作者论文） |

**特点**：
- **完全免费**，无需任何 API Key
- 返回标题、作者、期刊、摘要、被引量
- 覆盖中文学术核心期刊
- 适合中文文献调研

**搜索示例**：
```
websearch_web_search_exa "高温热泵 工业余热 论文 site:cnki.net OR site:cqvip.com OR site:wanfangdata.com.cn"
```

---

## 9. OpenAlex API

**端点**：`https://api.openalex.org/works`

**速率限制**：免费层慷慨，配邮件 Key 可入 polite pool

**数据规模**：250M+ 作品（论文/书籍/学位论文/数据集），100M 作者，2.5B 引用

**搜索**：
```
GET https://api.openalex.org/works?search={keywords}&per_page={n}&sort=cited_by_count:desc
```

**可用 filters**：`language`, `type`, `is_oa`, `publication_year`, `authorships.institutions.id`

**搜索示例**：
```bash
curl "https://api.openalex.org/works?search=high+temperature+heat+pump&per_page=5&sort=cited_by_count:desc"
```

**特点**：最大开放学术库（CC0）、全学科、⅓ 非英语、被莱顿排名采用、论文+书籍+学位论文混合索引
