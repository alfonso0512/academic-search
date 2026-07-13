---
name: academic-search
description: 学术论文垂直搜索。6 大权威数据源（Semantic Scholar / Crossref / PubMed / arXiv / Zenodo / 秘塔搜索），中英双路并行。免费可用，配 S2+秘塔 Key 体验最佳。
version: 2.0.0
author: 阿星
---

## 设计思想

6 大权威学术数据源，中英双路并行：

```
用户 "高温热泵论文"
        │
   ├──→ 🔬 Semantic Scholar     → 英文论文 + DOI + 引用次数
   │
   └──→ 🇨🇳 秘塔搜索            → 中文学术 + 产业报告
                 │
                 ▼
            合并呈现：双语学术搜索
```

## ⚡ 首次使用：配置 API Key（获得最佳体验）

**当用户安装本 Skill 后首次触发学术搜索时，执行以下流程：**

### Step 1：引导配置

> "为了给你最好的学术搜索体验，建议配置两个 Key——
>
> 1. **Semantic Scholar API Key**（推荐）
>    - 不配也能用，但免费层仅 100 次/5 分钟，容易限流
>    - 配 Key 后速率大幅提升，稳定高速
>    - 免费申请：https://www.semanticscholar.org/product/api#api-key-form
>
> 2. **秘塔学术 API Key**（必需）
>    - 不配的话中文搜索功能暂不可用
>    - 配 Key 后解锁中文学术/技术实时搜索
>
> 你有哪个 Key？直接告诉我，我帮你配置。"

### Step 2：写入 .env

| 用户答复 | 操作 |
|----------|------|
| "有 S2 Key: xxx" | 写入 `SEMANTIC_SCHOLAR_API_KEY=xxx` |
| "有秘塔 Key: xxx" | 写入 `METASO_API_KEY=xxx` |
| "两个都有" | 写入两个 |
| "都没有" | 使用 S2 免费层，秘塔暂不可用（可后期补配） |

### Step 3：确认

```
✅ 配置完成！

Semantic Scholar: [配 Key ✓  高速模式] / [免费层 100req/5min]
秘塔搜索:       [配 Key ✓  中文可用] / [未配置 ✗  仅英文]

后期补配 Key：编辑 <skill_dir>/.env
```

### 速率对比

| 源 | 无 Key | 有 Key |
|------|------|------|
| Semantic Scholar | 100req/5min（可能限流） | 高速，稳定 |
| 秘塔搜索 | ❌ 不可用 | ✅ 中文学术实时搜索 |
| Crossref | ✅ 免费无限 | — |
| PubMed | ✅ 3req/s | 10req/s |
| arXiv | ✅ 免费无限 | — |
| Zenodo | ✅ 免费无限 | — |

---

## 🌐 双路搜索（默认行为）

**每次学术搜索，中英双路并行——这是默认行为，不是可选项。**

```
用户 "高温热泵 学术论文"
        │
        ├──→ Semantic Scholar（英文论文）  ──→ 结构化元数据 + 引用次数
        │
        └──→ 秘塔搜索（中文学术）        ──→ 中文论文 + 产业报告
                    │
                    ▼
              合并呈现：英文学术 + 中文学术
```

### 执行规则

| 场景 | 行为 |
|------|------|
| 用户搜任意学术关键词 | **同时**调 S2 + 秘塔，并行返回 |
| 用户明确说"英文论文" | 只调 S2 |
| 用户明确说"中文论文" | 只调秘塔 |
| 秘塔未配置 Key | 只调 S2，并在结果末尾提示"配置秘塔 Key 可解锁中文学术搜索" |
| 用户搜 DOI/PMID 等精确标识符 | 只调 Crossref/PubMed（无需双路） |

### 输出格式

```
## 🔬 英文学术论文 (Semantic Scholar, N 条)
### 1. [标题]
- 期刊 / 引用次数 / DOI ...

## 🇨🇳 中文学术结果 (秘塔搜索, N 条)
### 1. [标题]
- 来源 / 摘要 ...
```

---

## 触发条件

当用户查询涉及以下场景时激活：

- "找论文"、"搜文献"、"有什么相关研究"、"最新论文"
- "DOI 查询"、"这篇论文的信息"、"被引次数"
- "PubMed 搜一下"、"生物医学文献"、"临床试验"
- "arXiv 预印本"、"最新 preprint"
- "研究数据集"、"dataset"

## 6 个子域 + 对应 API

| 子域 | API | 端点 | 用途 |
|------|-----|------|------|
| **papers** | Semantic Scholar | `api.semanticscholar.org` | 论文语义搜索（2 亿+ 论文） |
| **citation** | Crossref | `api.crossref.org` | DOI 元数据 / 引用关系 |
| **biomedical** | PubMed + Europe PMC | `eutils.ncbi.nlm.nih.gov` / `ebi.ac.uk` | 生物医学文献 |
| **preprint** | arXiv | `export.arxiv.org` | 预印本搜索 |
| **dataset** | Zenodo | `zenodo.org/api` | 研究数据集 |
| **metaso** | 秘塔搜索 | `metaso.cn/api/v1/search` | 中文学术/技术实时搜索 |

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

### 秘塔搜索（中文学术/技术）

```bash
curl -X POST "https://metaso.cn/api/v1/search" \
  -H "Authorization: Bearer $METASO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q":"固态电池 最新进展","n":5}'
```

覆盖中文学术论文、行业报告、技术博客、B站视频等实时内容。

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
