# MES BOM Optimization Skill

智能 MES BOM 生成引擎，为轨道交通装备制造提供完整的 BOM 数据生成服务。

## 📁 文件结构

```
skills/mes-bom-optimization/
├── SKILL.md              # 技能使用说明
├── README.md             # 本文件
├── mes_bom_generator.py  # 核心生成引擎
├── intelligent_bom_server.py  # HTTP API 服务
├── chat_demo.html        # 对话式界面示例
└── locomotive_harmony_bom.md  # 示例数据
```

## 🚀 快速开始

### 使用对话接口

直接告诉我：

```
生成火车车头的 BOM，产品编码：LOC-2026-001
```

我将自动生成完整的 BOM 数据，包含 3 张表：
- ✅ BOM 主表 (t_bom_main)
- ✅ BOM 明细表 (t_bom_details)
- ✅ 工序信息表 (t_operation)

### 支持的 product

- 🚂 **火车车头** - 柴油机车
- ⚡ **和谐型电力机车** - 交流传动电力机车
- 🏭 **装配线** - 通用装配生产线

## 🛠️ 技术实现

### 核心组件

1. **工艺知识库** - 预定义每种产品的完整工艺信息
2. **数据生成器** - 自动映射到 MES 表结构
3. **智能辅助** - 物料名称补全、外购件识别

### 数据格式

返回标准 JSON 结构，可直接导入 MES 系统：

```json
{
  "status": "success",
  "bom_code": "BOM-20260407-7852",
  "bom_main": {...},
  "bom_details": [...],
  "operations": [...],
  "summary": {...}
}
```

## 📊 生成内容

每个 BOM 包含：

### BOM 主表
- 产品基本信息
- 工艺描述
- 技术参数
- 质量标准

### BOM 明细表
- 按工序分类的物料
- 使用部位标注
- 外购/自制标识
- 数量、单位、损耗率

### 工序信息表
- 工序编码、名称
- 所需设备清单
- 预计工时
- 人员要求
- 质量控制点

## 🔧 扩展

### 添加新产品

在 `mes_bom_generator.py` 中添加：

```python
PROCESS_KNOWLEDGE["新产品"] = {
    "工艺描述": "...",
    "工艺流程": [
        {
            "operation_code": "OP-001",
            "operation_name": "工序名称",
            "required_materials": [...],
            ...
        }
    ],
    "technical_parameters": {...},
    "quality_standards": {...}
}
```

### 添加物料

在 `MATERIAL_NAMES` 字典中添加物料名称映射。

## 📝 示例数据

查看 `locomotive_harmony_bom.md` 获取完整的示例输出。

## 🌐 API 接口

启动 HTTP 服务：

```bash
python intelligent_bom_server.py
```

API 端点：`POST /api/generate/bom`

## 🎯 使用场景

- 制造 BOM 生成
- 工艺路线规划
- 物料需求计划
- MES 系统导入

---

**Ready to generate?** Just ask!
