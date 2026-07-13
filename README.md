# Academic Search — 学术论文搜索 Skill

> 直连学术 API 免费层，零外部依赖。Semantic Scholar + Crossref + PubMed + arXiv + Zenodo。

## 设计思想

```
用户 "固态电池最新论文"
        │
        ▼
  直连 Semantic Scholar API（免费层）
        │
        ▼
  返回结构化 JSON：标题 / 作者 / DOI / 引用次数
```

不依赖 anysearch、不依赖 API Key。所有 API 均有免费层。

## 5 个搜索能力

| 子域 | API | 用途 |
|------|-----|------|
| **papers** | Semantic Scholar | 2 亿+ 论文语义搜索 |
| **citation** | Crossref | DOI 元数据 + 引用关系 |
| **biomedical** | PubMed + Europe PMC | 生物医学文献 |
| **preprint** | arXiv | 最新预印本 |
| **dataset** | Zenodo | 研究数据集 |

## 安装

```bash
git clone https://github.com/YOUR_USERNAME/academic-search.git ~/.config/opencode/skills/academic-search
```

零配置、零 API Key。开箱即用。

## 使用示例

```
"固态电池最新论文"          → Semantic Scholar
"这篇 DOI 的详细信息"        → Crossref
"PubMed 搜 mRNA 疫苗"        → PubMed
"arXiv 最新 LLM 预印本"      → arXiv
"气候变化数据集"             → Zenodo
```

## 文件结构

```
academic-search/
├── README.md
├── SKILL.md
├── references/
│   └── apis.md      # 6 个 API 的完整文档
└── .gitignore
```

## 许可

MIT
