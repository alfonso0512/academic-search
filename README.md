# Academic Search — 学术论文搜索 Skill

> 中英双路学术搜索，免费开箱即用。配 Key 体验更佳。

## 开箱即用

安装后直接搜——中英双路并行，**无需配置任何 Key**：

```
"固态电池最新论文"
        │
   ├──→ 🔬 Semantic Scholar     → 英文论文 + 引用次数 + DOI
   │
   └──→ 🇨🇳 中文学术站点        → 知网 / 万方 / 维普 / 百度学术
                 │
                 ▼
            双语结果同屏呈现
```

## 免费 vs 配 Key

| | 默认（免费） | 配 Key 后 |
|------|------|------|
| 英文论文搜索 | ✅ S2 + OpenAlex | ✅ 高速不限流 |
| 中文论文搜索 | ✅ 知网/万方/维普/百度学术 | ✅ 秘塔实时搜索（更广更深） |
| DOI 查询 | ✅ Crossref | — |
| 生物医学 | ✅ PubMed | ✅ 提速至 10req/s |
| 预印本 | ✅ arXiv | — |
| 数据集 | ✅ Zenodo | — |

> 💡 **建议配置的 Key**：[Semantic Scholar](https://www.semanticscholar.org/product/api#api-key-form)（免费申请，解除限流）| 秘塔学术（中文搜索升级）

## 安装

```bash
git clone https://github.com/alfonso0512/academic-search.git ~/.config/opencode/skills/academic-search
```

首次使用时会引导你配置 Key，也可以跳过，后期随时在 `.env` 里补配。

## 使用示例

```
"固态电池最新论文"         → S2 英文 + 知网/万方中文（双路并行）
"高温热泵 工业应用"        → 中英双语学术搜索
"这篇 DOI 的详细信息"      → Crossref
"PubMed 搜 mRNA 疫苗"      → PubMed
"arXiv 最新 LLM 预印本"    → arXiv
```

## 许可

MIT
