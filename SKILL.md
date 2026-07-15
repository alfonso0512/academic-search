---
name: academic-search
description: 学术论文垂直搜索。8 大权威数据源（S2/OpenAlex/知网万方维普/Crossref/PubMed/arXiv/Zenodo/秘塔），中英双路并行。免费可用，配 Key 体验最佳。
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

### Step 1：引导配置（可跳过）

> "学术搜索已就绪——中英双路并行，免费开箱即用。
>
> 如果想获得更好的体验，可以配置 Key（可选，随时可补）：
>
> 1. **Semantic Scholar Key**：解除 100次/5分钟限流 → 高速稳定
> 2. **秘塔学术 Key**：升级中文搜索质量（更广更深）
> 3. **OpenAlex Key**：解锁最大开放学术库（2.5亿+，全学科）
>
> 现在配还是先用着？直接告诉我就行。"

### Step 2：写入 .env

| 用户答复 | 操作 |
|----------|------|
| "有 S2 Key: xxx" | 写入 `SEMANTIC_SCHOLAR_API_KEY=xxx` |
| "有秘塔 Key: xxx" | 写入 `METASO_API_KEY=xxx` |
| "两个都有" | 写入两个 |
| "都没有" | 使用 S2 免费层，秘塔暂不可用（后期随时补配） |

### Step 3：确认

```
✅ 配置完成！

Semantic Scholar: [配 Key ✓  高速模式] / [免费层 100req/5min]
秘塔搜索:       [配 Key ✓  中文可用] / [未配置 ✗  仅英文（可后期补配）]

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
用户 "高温热泵论文"
        │
   ├──→ 🔬 Semantic Scholar     → 英文论文 + DOI + 引用次数
   │
   └──→ 🇨🇳 Exa + 中文学术站点   → 免费中文论文（知网/万方/维普/百度学术）
                 │
                 ▼
            合并呈现：双语学术搜索
```

### 执行规则

| 场景 | 行为 |
|------|------|
| 用户搜任意学术关键词 | **同时**调英文路 + 中文路，并行返回 |
| 用户明确说"英文论文" | 只调英文路 |
| 用户明确说"中文论文" | 只调中文路 |

### 降级策略

```
                    ┌── 英文路 ──────────────────────┐
                    │                                  │
用户搜 "关键词" ───┤   1. Semantic Scholar（主）       │
                    │      ↓ 限流/故障                 │
                    │   2. OpenAlex（降级）             │
                    │      ↓ 也挂了                     │
                    │   3. 仅返回中文结果 + 报错提示     │
                    │                                  │
                    └── 中文路 ──────────────────────┘
                           │
                     有秘塔Key？
                      ├── 是 → 秘塔搜索（主）
                      │         ↓ 故障
                      │       papers_zh（降级）
                      │
                      └── 否 → papers_zh（Exa + 知网/万方/维普）
                                ↓ Exa 不可用
                               仅返回英文结果 + 提示
```

| 降级路径 | 触发条件 | 效果 |
|------|------|------|
| S2 → OpenAlex | S2 429 限流 / 超时 | 用 OpenAlex 继续搜英文 |
| 秘塔 → papers_zh | 秘塔 API 故障 | 回退免费中文搜索 |
| papers_zh → 跳过中文 | Exa 不可用 | 仅英文结果 + 提示 "配置秘塔 Key 解锁中文" |
| 全部不可用 → 报错 | 罕见 | 提示用户检查网络

### 输出格式

```
## 🔬 英文学术论文 (Semantic Scholar, N 条)
### 1. [标题]
- 期刊 / 引用次数 / DOI ...

## 🇨🇳 中文学术结果 (papers_zh, N 条)
### 1. [标题]
- 来源 / 摘要 / 链接 ...
```

---

## 触发条件

当用户查询涉及以下场景时激活：

- "找论文"、"搜文献"、"有什么相关研究"、"最新论文"
- "DOI 查询"、"这篇论文的信息"、"被引次数"
- "PubMed 搜一下"、"生物医学文献"、"临床试验"
- "arXiv 预印本"、"最新 preprint"
- "研究数据集"、"dataset"

## 8 大搜索源

| 源 | 后端 | Key | 用途 |
|------|------|:--:|------|
| **papers** | Semantic Scholar | 推荐 | 英文学术论文（2 亿+） |
| **openalex** | OpenAlex | 可选 | 最大开放学术库（2.5 亿+，全学科） |
| **papers_zh** | Exa + 中文学术站点 | 无需 | 免费中文论文（知网/万方/维普/百度学术） |
| **citation** | Crossref | 无需 | DOI 元数据 + 引用关系 |
| **biomedical** | PubMed + Europe PMC | 无需 | 生物医学文献 |
| **preprint** | arXiv | 无需 | 最新预印本 |
| **dataset** | Zenodo | 无需 | 研究数据集 |
| **metaso** | 秘塔搜索 | 推荐 | 中文学术/技术实时搜索 |

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

### 免费中文论文搜索（Exa + 中文学术站点）

使用 `websearch_web_search_exa` + 中文学术站点过滤，免费且无需任何 Key：

```
site:cnki.net OR site:xueshu.baidu.com OR site:wanfangdata.com.cn OR site:cqvip.com OR site:arxiv.org
```

**Agent 调用**：
```
websearch_web_search_exa "高温热泵 工业 论文 site:cnki.net OR site:cqvip.com OR site:wanfangdata.com.cn OR site:xueshu.baidu.com OR site:arxiv.org"
```

覆盖知网、万方、维普、百度学术、arXiv。返回标题、作者、期刊、摘要、引用量。

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
