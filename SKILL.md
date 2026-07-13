---
name: academic-search
description: 学术论文垂直搜索。直连 Semantic Scholar、Crossref、PubMed、arXiv、Zenodo 等学术 API（免费层），无外部依赖。支持论文搜索、DOI 查询、引用关系、生物医学文献、预印本、数据集。
version: 2.0.0
author: 阿星
---

## 设计思想

直连学术数据库 API 免费层，零依赖：

```
用户 "固态电池最新论文"
        │
        ▼
  识别 → Semantic Scholar API
        │
        ▼
  curl/wget → api.semanticscholar.org
        │
        ▼
  返回 JSON：标题 / 作者 / DOI / 引用次数
```

**与 v1.0 的差异**：

| | v1.0（废弃） | v2.0（当前） |
|------|------|------|
| 后端 | anysearch 代理 | 直连学术 API |
| 依赖 | anysearch | **零外部依赖** |
| 认证 | anysearch Key | 全部免费层（无需任何 Key） |
| 可控性 | 黑盒代理 | 透明，可调参数 |

## 触发条件

当用户查询涉及以下场景时激活：

- "找论文"、"搜文献"、"有什么相关研究"、"最新论文"
- "DOI 查询"、"这篇论文的信息"、"被引次数"
- "PubMed 搜一下"、"生物医学文献"、"临床试验"
- "arXiv 预印本"、"最新 preprint"
- "研究数据集"、"dataset"

## 5 个子域 + 对应 API

| 子域 | API | 端点 | 用途 |
|------|-----|------|------|
| **papers** | Semantic Scholar | `api.semanticscholar.org` | 论文语义搜索（2 亿+ 论文） |
| **citation** | Crossref | `api.crossref.org` | DOI 元数据 / 引用关系 |
| **biomedical** | PubMed + Europe PMC | `eutils.ncbi.nlm.nih.gov` / `ebi.ac.uk` | 生物医学文献 |
| **preprint** | arXiv | `export.arxiv.org` | 预印本搜索 |
| **dataset** | Zenodo | `zenodo.org/api` | 研究数据集 |

完整 API 文档见 `references/apis.md`。

## 使用方法

### 论文语义搜索（Semantic Scholar）

```
GET https://api.semanticscholar.org/graph/v1/paper/search?query={url_encoded_query}&limit=10&fields=title,authors,year,citationCount,journal,externalIds
```

**用 webfetch**：
```
webfetch "https://api.semanticscholar.org/graph/v1/paper/search?query=solid+state+battery+electrolyte&limit=5&fields=title,authors,year,citationCount,journal,externalIds"
```

**用 curl**：
```bash
curl "https://api.semanticscholar.org/graph/v1/paper/search?query=solid+state+battery&limit=5&fields=title,authors,year,citationCount,journal,externalIds"
```

**速率限制**：100req/5min（免费），有 Key 更高

### DOI 精准查询（Crossref）

```bash
curl "https://api.crossref.org/works/10.1038/s41586-021-03819-2"
```

返回完整元数据：标题、作者、期刊、日期、摘要、参考文献列表、被引次数。

### 生物医学搜索（PubMed）

```bash
# Step 1: 搜索
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=mRNA+vaccine+cancer&retmax=5&retmode=json"
# Step 2: 获取详情
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=<PMID>&retmode=json"
```

### 生物医学搜索（Europe PMC，更简单）

```bash
curl "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=COVID-19+vaccine&resultType=core&pageSize=5&format=json"
```

### 预印本搜索（arXiv）

```bash
curl "http://export.arxiv.org/api/query?search_query=all:large+language+model+reasoning&start=0&max_results=5&sortBy=submittedDate&sortOrder=descending"
```

### 数据集搜索（Zenodo）

```bash
curl "https://zenodo.org/api/records?q=climate+temperature+dataset&size=5"
```

## 输出格式

结果以结构化方式呈现：

```
## [数据源] 搜索结果 (N 条)

### 1. [标题]
- 作者: [作者列表]
- 期刊/年份: [Venue] ([Year])
- DOI: [DOI]
- 引用次数: [N]（仅 Semantic Scholar）
- 链接: [URL]
```

## 示例会话

**用户**: "固态电池最新论文有哪些？"

**Agent 执行**:
```bash
curl "https://api.semanticscholar.org/graph/v1/paper/search?query=solid+state+battery+electrolyte&limit=10&fields=title,authors,year,citationCount,journal,externalIds"
```

**用户**: "这篇论文的信息？DOI: 10.1038/s41586-021-03819-2"

**Agent 执行**:
```bash
curl "https://api.crossref.org/works/10.1038/s41586-021-03819-2"
```

**用户**: "PubMed 上搜一下 mRNA 癌症疫苗"

**Agent 执行**:
```bash
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=mRNA+vaccine+cancer&retmax=10&retmode=json"
```

**用户**: "arXiv 上 MoE 架构有什么新预印本？"

**Agent 执行**:
```bash
curl "http://export.arxiv.org/api/query?search_query=all:mixture+of+experts+language+model&start=0&max_results=5"
```

## 扩展指南

添加新 API 只需两步：
1. 在 `references/apis.md` 添加 API 文档
2. 在本文档子域表中添加对应行
