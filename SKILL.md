# 智能工艺 BOM 生成器

## 简介

专业的 MES BOM 生成工具，只返回纯 JSON 格式数据用于入库。

## 核心功能

**唯一功能：BOM 生成**

1. 从工艺知识库查找产品信息
2. 生成标准 BOM JSON
3. 未找到时由大模型生成

## 输出格式

**只返回纯 JSON 字符串，无任何额外文本、总结或说明。**

```json
{"status": "success", "bom_code": "...", "bom_main": {...}, "bom_details": [...], "operations": [...], "summary": {...}}
```

## 使用方式

### 输入

```
生成火车车头的 BOM，产品编码：LOC-2026-001
```

### 输出

纯 JSON 字符串：

```json
{"status":"success","bom_code":"BOM-20260407-XXXX","bom_main":{...},"bom_details":[...],"operations":[...],"summary":{...}}
```

## 支持的產品

- 🚂 火车车头
- ⚡ 和谐型电力机车
- 🏭 装配线
- 🚒 消防水炮车
- 🔥 消防喷头

## 处理流程

1. **查找数据库** - 从内置知识库查找工艺信息
2. **生成 JSON** - 生成标准 BOM 数据
3. **返回纯 JSON** - 无任何额外文本

如果数据库未找到：
1. **由大模型生成** - 直接调用大模型生成完整 JSON

## 文件结构

```
skills/mes-bom-optimization/
├── SKILL.md
├── bom_generator.py   # 核心生成器
└── bom_skill.py       # 技能入口
```

---

**需要生成 BOM？告诉我产品名称和编码！**

**只返回纯 JSON，无任何额外文本。**
