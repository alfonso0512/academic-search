# Academic Search — 学术论文搜索 Skill

> 6 大权威学术数据源，中英双路并行搜索。免费可用，配 Key 体验更佳。

## 设计思想

```
用户 "固态电池最新论文"
        │
   ├──→ Semantic Scholar（英文学术论文）
   │      └─ 期刊 / DOI / 引用次数
   │
   └──→ 秘塔搜索（中文学术+产业）
          └─ 中文论文 / 行业报告 / 技术博客
                 │
                 ▼
            合并呈现：中英双路
```

## 7 大搜索数据源

| 源 | 能力 | Key |
|------|------|:--:|
| **Semantic Scholar** | 2 亿+ 论文语义搜索 | 推荐配 |
| **中文学术站点** | 知网/万方/维普/百度学术 | **免费** |
| **Crossref** | DOI 元数据 + 引用关系 | 无需 |
| **PubMed** | 生物医学文献 + MeSH | 无需 |
| **arXiv** | 最新预印本 | 无需 |
| **Zenodo** | 研究数据集 | 无需 |
| **秘塔搜索** | 中文学术/技术实时搜索 | 推荐配 |

> 💡 **配 Key 体验最佳**：Semantic Scholar 免费层 100 次/5 分钟（易限流），秘塔搜索需 Key 才能启用。建议申请：[S2 Key](https://www.semanticscholar.org/product/api#api-key-form) | 秘塔 Key（联系官方）。

## 安装

```bash
git clone https://github.com/alfonso0512/academic-search.git ~/.config/opencode/skills/academic-search
```

首次使用时会引导你配置 Key，也可以直接编辑 `.env` 文件。

## 使用示例

```
"固态电池最新论文"           → S2 英文 + 秘塔中文（双路并行）
"这篇 DOI 的详细信息"         → Crossref
"PubMed 搜 mRNA 疫苗"         → PubMed
"arXiv 最新 LLM 预印本"       → arXiv
"气候变化数据集"              → Zenodo
```

## 文件结构

```
academic-search/
├── README.md
├── SKILL.md
├── .env.example
├── references/
│   └── apis.md              # 7 个 API 完整文档
└── scripts/
    └── academic_search.py   # 统一 CLI（6 源后端）
```

## 许可

MIT
