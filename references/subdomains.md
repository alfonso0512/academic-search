# 学术搜索子域参考

> 本文档等价于 anysearch 的 `get_sub_domains --domain academic` 返回结果。每个子域列出数据源、参数和搜索示例。

## 子域总览

| # | 子域 | 中文名 | 数据源 | 核心能力 |
|---|------|--------|--------|----------|
| 1 | academic.search | 论文语义搜索 | Semantic Scholar | 关键词→论文，带引用计数 |
| 2 | academic.citation | 引用关系查询 | Crossref + OpenAlex | DOI→元数据/被引/参考文献 |
| 3 | academic.biomedical | 生物医学文献 | PubMed + Europe PMC | MeSH 词表、临床试验 |
| 4 | academic.preprint | 预印本搜索 | arXiv + Semantic Scholar | 最新未发表研究 |
| 5 | academic.dataset | 研究数据集 | Zenodo | DOI 标识的研究数据 |

---

## 1. academic.search（论文语义搜索）

**数据源**：Semantic Scholar（2 亿+ 论文，Allen Institute for AI）

**能力**：
- 自然语言关键词搜索论文
- 返回 DOI、作者、期刊、年份、引用次数
- 支持语义理解（非简单关键词匹配）

**搜索示例**：
```bash
<anysearch-cli> search "solid state battery electrolyte interface" \
  --domain academic \
  --sub_domain academic.search
```

**典型返回**：
```
### 1. High-power all-solid-state batteries using sulfide superionic conductors
- DOI: 10.1038/nenergy.2016.30
- Authors: Yuki Kato, Satoshi Hori, Toshiya Saito, et al.
- Venue: Nature Energy (2016)
- Cited: 3451 times
```

---

## 2. academic.citation（引用关系查询）

**数据源**：Crossref（1.5 亿+ 元数据记录）+ OpenAlex（2.5 亿+ 学术作品）

**能力**：
| 操作 (op) | 功能 | 示例场景 |
|-----------|------|----------|
| `metadata` | 根据 DOI/PMID 获取论文元数据 | "这篇论文的基本信息" |
| `citations` | 查询被哪些论文引用 | "AlphaFold 被引用了多少次？被谁引用？" |
| `references` | 查询论文引用了哪些文献 | "这篇论文的参考文献列表" |
| `citation-count` | 只返回引用次数 | "这篇论文被引了多少次？" |
| `reference-count` | 只返回参考文献数量 | "这篇论文引用了多少文献？" |
| `author` | 根据 ORCID 查作者作品 | "这个作者发表了哪些论文？" |

**参数**：

| 参数 | 必需 | 说明 | 示例 |
|------|:--:|------|------|
| `id` | ✅ | DOI/PMID/ISSN/ISBN/ORCID/OCI | `10.1038/s41586-021-03819-2` |
| `op` | ❌ | 操作类型，默认 `metadata` | `citations` / `references` / `citation-count` |
| `id_type` | ❌ | 标识符类型，留空自动检测 | `doi` / `pmid` / `orcid` |
| `year_from` | ❌ | 发表年份下限 | `2023` |
| `year_to` | ❌ | 发表年份上限 | `2026` |
| `min_citations` | ❌ | 最小引用数过滤 | `100` |
| `open_access` | ❌ | 只看开放获取 | `true` |
| `venue` | ❌ | 期刊/会议名 | `Nature` / `NeurIPS` / `ICML` |
| `category` | ❌ | 学科分类（22 个） | `Computer Science` / `Medicine` |
| `type` | ❌ | 文献类型 | `journal-article` / `proceedings-article` / `posted-content` |
| `filter` | ❌ | RAMOSE 过滤表达式 | `creation:2020-*-*` |
| `sort` | ❌ | RAMOSE 排序表达式 | `creation:desc` |

**学科分类（22 个）**：
```
Computer Science, Medicine, Biology, Chemistry, Physics, Mathematics,
Materials Science, Engineering, Environmental Science, Geology, Geography,
Sociology, Psychology, Economics, Business, Political Science, Linguistics,
Philosophy, History, Art, Education, Law
```

**搜索示例**：

```bash
# 查论文元数据
<anysearch-cli> search "10.1038/s41586-021-03819-2" \
  --domain academic \
  --sub_domain academic.citation \
  --sub_domain_params '{"id":"10.1038/s41586-021-03819-2","op":"metadata"}'

# 查被引用列表（近 3 年、CS 领域、引用 >50）
<anysearch-cli> search "alphaFold citations" \
  --domain academic \
  --sub_domain academic.citation \
  --sub_domain_params '{"id":"10.1038/s41586-021-03819-2","op":"citations","year_from":"2023","category":"Computer Science","min_citations":"50"}'

# 查某作者的论文（ORCID）
<anysearch-cli> search "author works" \
  --domain academic \
  --sub_domain academic.citation \
  --sub_domain_params '{"id":"0000-0003-2812-9917","op":"author","id_type":"orcid"}'
```

---

## 3. academic.biomedical（生物医学文献）

**数据源**：PubMed（3700 万+ 生物医学文献）+ Europe PMC

**能力**：
- 生物医学关键词搜索
- 返回 MeSH 词表、临床试验信息、PMCID
- 作者 ORCID、所属机构
- 完整摘要

**搜索示例**：
```bash
<anysearch-cli> search "COVID-19 vaccine efficacy mRNA" \
  --domain academic \
  --sub_domain academic.biomedical
```

**典型返回**：
```
### 1. Host factors and vaccine efficacy: Implications for COVID-19 vaccines
- Authors: Shahab Falahi (ORCID: 0000-0002-3764-2168), Azra Kenarkoohi
- Journal: Journal of Medical Virology, 94(4):1330-1335 (2022)
- DOI: 10.1002/jmv.27485
- PMCID: PMC9015327
- MeSH Terms: COVID-19/immunology, Vaccine Efficacy*, SARS-CoV-2/genetics
- Publication Types: Journal Article, Review
```

---

## 4. academic.preprint（预印本搜索）

**数据源**：arXiv（250 万+ 预印本）+ Semantic Scholar

**能力**：
- 搜索尚未正式发表的最新研究
- 返回 DOI、引用次数（来自 S2）
- 覆盖：物理、数学、CS、生物、金融等领域

**搜索示例**：
```bash
<anysearch-cli> search "large language model reasoning chain of thought" \
  --domain academic \
  --sub_domain academic.preprint
```

---

## 5. academic.dataset（研究数据集）

**数据源**：Zenodo（CERN 运营，百万级研究数据）

**能力**：
- 搜索研究数据集（非论文）
- DOI 标识、可引用
- 覆盖全学科

**搜索示例**：
```bash
<anysearch-cli> search "global temperature climate dataset" \
  --domain academic \
  --sub_domain academic.dataset
```

---

## anysearch CLI 调用参考

### 基础语法
```bash
# Python runtime
python <skill_dir>/scripts/anysearch_cli.py search "query" \
  --domain academic \
  --sub_domain academic.<subdomain> \
  --sub_domain_params '<json_params>'

# Node.js runtime
node <skill_dir>/scripts/anysearch_cli.js search "query" \
  --domain academic \
  --sub_domain academic.<subdomain> \
  --sub_domain_params '<json_params>'

# PowerShell runtime
<anysearch-cli> search "..." \
  --domain academic \
  --sub_domain academic.<subdomain> \
  --sub_domain_params '<json_params>'
```

### 批量搜索（跨子域并行）
```bash
<anysearch-cli> batch_search --queries '[
  {"query":"solid state battery","sub_domain":"academic.search"},
  {"query":"10.1038/s41586-021-03819-2","sub_domain":"academic.citation",
   "sub_domain_params":{"op":"citation-count"}},
  {"query":"global temperature dataset","sub_domain":"academic.dataset"}
]'
```

## 数据源详解

| 数据源 | 运营方 | 规模 | 更新频率 | API 类型 |
|--------|--------|------|----------|----------|
| **Semantic Scholar** | Allen Institute for AI | 2 亿+ 论文 | 每日 | 免费 REST API |
| **Crossref** | PILA（非营利） | 1.5 亿+ 元数据 | 实时 | 免费 REST API |
| **OpenAlex** | OurResearch（非营利） | 2.5 亿+ 作品 | 每两周 | 免费 REST API |
| **PubMed** | NCBI/NLM（美国政府） | 3700 万+ 文献 | 每日 | 免费 E-utilities API |
| **Europe PMC** | EMBL-EBI（欧盟） | 4200 万+ 摘要 | 每日 | 免费 REST API |
| **arXiv** | Cornell University | 250 万+ 预印本 | 每日 | 免费 OAI-PMH API |
| **Zenodo** | CERN（欧盟） | 百万级数据集 | 实时 | 免费 REST API |
