#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
消防喷头 BOM 生成器
"""

import json
import datetime
import random

# ============== 消防喷头工艺知识库 ==============

SPRINKLER_PROCESS_DATA = {
    "product_name": "消防喷头",
    "process_keyword": "消防喷头，sprinkler head, 喷淋头",
    "process_description": "消防喷头是自动喷水灭火系统的末端执行机构，通过热敏元件感知火灾温度，自动开启喷水灭火。采用精密铸造工艺，确保密封性能和喷水效果。",
    
    "工艺流程": [
        {
            "operation_code": "OP-001",
            "operation_name": "零部件铸造",
            "description": "铸造喷头主体、盖板和框架等零部件。",
            "required_materials": [
                {"material_code": "MAT-S001", "quantity": 5.0, "unit": "KG", "usage_point": "整工序消耗"},
                {"material_code": "MAT-S002", "quantity": 0.5, "unit": "KG", "usage_point": "铸造材料"}
            ],
            "required_equipment": ["精密铸造机", "热处理炉", "检测设备"],
            "estimated_time": "6-8 小时",
            "personnel_requirement": "2-3 名技工",
            "quality_control": "尺寸检测、外观检查"
        },
        {
            "operation_code": "OP-002",
            "operation_name": "热敏元件装配",
            "description": "安装玻璃球或易熔合金热敏元件。",
            "required_materials": [
                {"material_code": "MAT-S003", "quantity": 100.0, "unit": "PC", "usage_point": "整工序装配"},
                {"material_code": "MAT-S004", "quantity": 50.0, "unit": "PC", "usage_point": "密封垫片"},
                {"material_code": "MAT-S005", "quantity": 10.0, "unit": "L", "usage_point": "密封胶"}
            ],
            "required_equipment": ["精密装配台", "压力测试仪"],
            "estimated_time": "4-6 小时",
            "personnel_requirement": "2-3 名装配技师",
            "quality_control": "密封性测试、开启温度验证"
        },
        {
            "operation_code": "OP-003",
            "operation_name": "螺纹加工",
            "description": "加工连接螺纹，确保与管道的密封配合。",
            "required_materials": [
                {"material_code": "MAT-S006", "quantity": 2.0, "unit": "L", "usage_point": "冷却液"},
                {"material_code": "MAT-S007", "quantity": 0.5, "unit": "KG", "usage_point": "切削液"}
            ],
            "required_equipment": ["数控车床", "螺纹规", "表面粗糙度仪"],
            "estimated_time": "3-5 小时",
            "personnel_requirement": "2 名技工",
            "quality_control": "螺纹精度检测、表面质量检查"
        },
        {
            "operation_code": "OP-004",
            "operation_name": "表面处理",
            "description": "进行镀锌或镀铬处理，提高耐腐蚀性能。",
            "required_materials": [
                {"material_code": "MAT-S008", "quantity": 1.0, "unit": "KG", "usage_point": "镀锌材料"},
                {"material_code": "MAT-S009", "quantity": 50.0, "unit": "L", "usage_point": "处理液"},
                {"material_code": "MAT-S010", "quantity": 20.0, "unit": "L", "usage_point": "清洗剂"}
            ],
            "required_equipment": ["电镀槽", "烘烤设备", "盐雾试验箱"],
            "estimated_time": "8-12 小时",
            "personnel_requirement": "3-4 名技工",
            "quality_control": "盐雾试验、镀层厚度检测"
        },
        {
            "operation_code": "OP-005",
            "operation_name": "总装配",
            "description": "完成喷头所有零部件的组装和最终调试。",
            "required_materials": [
                {"material_code": "MAT-S011", "quantity": 50.0, "unit": "PC", "usage_point": "装饰盖板"},
                {"material_code": "MAT-S012", "quantity": 30.0, "unit": "M", "usage_point": "保护套管"},
                {"material_code": "MAT-S013", "quantity": 5.0, "unit": "L", "usage_point": "润滑油"}
            ],
            "required_equipment": ["装配工作台", "压力测试台", "校准设备"],
            "estimated_time": "6-8 小时",
            "personnel_requirement": "3-4 名装配技师",
            "quality_control": "喷水角度校准、密封性最终测试"
        },
        {
            "operation_code": "OP-006",
            "operation_name": "性能测试",
            "description": "进行喷水特性测试和温度响应测试。",
            "required_materials": [
                {"material_code": "MAT-S014", "quantity": 1000.0, "unit": "L", "usage_point": "测试用水"},
                {"material_code": "MAT-S015", "quantity": 10.0, "unit": "L", "usage_point": "清洗剂"}
            ],
            "required_equipment": ["喷水试验台", "流量测试仪", "温度测试柜"],
            "estimated_time": "4-6 小时",
            "personnel_requirement": "2-3 名测试工程师",
            "quality_control": "K 值验证、响应时间测试"
        },
        {
            "operation_code": "OP-007",
            "operation_name": "包装入库",
            "description": "进行清洁、包装和入库前的最终检查。",
            "required_materials": [
                {"material_code": "MAT-S016", "quantity": 200.0, "unit": "PC", "usage_point": "包装材料"},
                {"material_code": "MAT-S017", "quantity": 50.0, "unit": "PC", "usage_point": "标识标签"},
                {"material_code": "MAT-S018", "quantity": 10.0, "unit": "L", "usage_point": "清洁剂"}
            ],
            "required_equipment": ["包装机", "检验台", "标签打印机"],
            "estimated_time": "3-5 小时",
            "personnel_requirement": "2-3 名包装工",
            "quality_control": "外观检查、包装完整性验证"
        }
    ],
    
    "technical_parameters": {
        "K 系数": "80 或 115",
        "工作压力": "0.05-1.2 MPa",
        "动作温度": "57°C/68°C/79°C/93°C",
        "响应时间": "≤75 秒 (RTI≤50)",
        "连接螺纹": "G1/2\" / 3/4\"",
        "洒水角度": "360°/180°/90°",
        "防护等级": "IP65"
    },
    
    "quality_standards": {
        "产品标准": "GB 5135.1-2019",
        "测试标准": "GB 5135.2-2003",
        "消防标准": "GA 112-2014",
        "验收标准": "自动喷水灭火系统施工及验收规范"
    }
}

# ============== 物料名称映射 ==============

SPRINKLER_MATERIAL_NAMES = {
    # 零部件
    "MAT-S001": "黄铜棒材 H59",
    "MAT-S002": "铸造石膏",
    
    # 热敏元件
    "MAT-S003": "玻璃球热敏元件",
    "MAT-S004": "橡胶密封垫片",
    "MAT-S005": "厌氧密封胶",
    
    # 加工材料
    "MAT-S006": "切削冷却液",
    "MAT-S007": "工业切削液",
    
    # 表面处理
    "MAT-S008": "镀锌材料",
    "MAT-S009": "电镀处理液",
    "MAT-S010": "工业清洗剂",
    
    # 装配材料
    "MAT-S011": "装饰盖板",
    "MAT-S012": "塑料保护套管",
    "MAT-S013": "锂基润滑脂",
    
    # 测试材料
    "MAT-S014": "去离子水",
    "MAT-S015": "表面清洁剂",
    
    # 包装材料
    "MAT-S016": "纸箱包装材料",
    "MAT-S017": "产品标识标签",
    "MAT-S018": "无水乙醇"
}

# ============== 外购件标识 ==============

SPRINKLER_PURCHASED_PARTS = [
    "MAT-S003",  # 玻璃球热敏元件
    "MAT-S004",  # 橡胶密封垫片
    "MAT-S011",  # 装饰盖板
    "MAT-S012",  # 保护套管
]


def generate_spinkler_bom(product_code: str = "SPR-2026-001") -> dict:
    """
    生成消防喷头 BOM
    
    Args:
        product_code: 产品编码
    
    Returns:
        标准化 BOM 数据
    """
    # 生成 BOM 编码
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    random_suffix = random.randint(1000, 9999)
    bom_code = f"BOM-{timestamp}-{random_suffix}"
    
    # 生成 BOM 主表
    bom_main = {
        "bom_code": bom_code,
        "product_name": SPRINKLER_PROCESS_DATA["product_name"],
        "product_code": product_code,
        "process_description": SPRINKLER_PROCESS_DATA["process_description"],
        "technical_parameters": json.dumps(SPRINKLER_PROCESS_DATA["technical_parameters"], ensure_ascii=False),
        "quality_standards": json.dumps(SPRINKLER_PROCESS_DATA["quality_standards"], ensure_ascii=False),
        "status": "active",
        "version": "1.0",
        "created_by": "MES_BOM_Generator_v1.0"
    }
    
    # 生成 BOM 明细表
    bom_details = []
    for operation in SPRINKLER_PROCESS_DATA["工艺流程"]:
        for material in operation["required_materials"]:
            bom_detail = {
                "bom_code": bom_code,
                "operation_code": operation["operation_code"],
                "operation_name": operation["operation_name"],
                "material_code": material["material_code"],
                "material_name": SPRINKLER_MATERIAL_NAMES.get(material["material_code"], material["material_code"]),
                "quantity": material["quantity"],
                "unit": material["unit"],
                "usage_point": material["usage_point"],
                "is_purchased": material["material_code"] in SPRINKLER_PURCHASED_PARTS,
                "standard_consumption": material["quantity"],
                "loss_rate": 0.02,
                "effective_date": datetime.datetime.now().date().isoformat(),
                "remark": f"用于{operation['operation_name']}"
            }
            bom_details.append(bom_detail)
    
    # 生成工序信息表
    operations = []
    for idx, operation in enumerate(SPRINKLER_PROCESS_DATA["工艺流程"], 1):
        operation_data = {
            "bom_code": bom_code,
            "operation_code": operation["operation_code"],
            "operation_name": operation["operation_name"],
            "description": operation["description"],
            "required_equipment": json.dumps(operation["required_equipment"], ensure_ascii=False),
            "estimated_time": operation["estimated_time"],
            "personnel_requirement": operation["personnel_requirement"],
            "quality_control": operation["quality_control"],
            "sequence": idx
        }
        operations.append(operation_data)
    
    # 汇总统计
    summary = {
        "total_materials": len(bom_details),
        "total_operations": len(operations),
        "purchased_parts": sum(1 for d in bom_details if d["is_purchased"]),
        "self_made_parts": sum(1 for d in bom_details if not d["is_purchased"])
    }
    
    return {
        "status": "success",
        "bom_code": bom_code,
        "bom_main": bom_main,
        "bom_details": bom_details,
        "operations": operations,
        "summary": summary
    }


if __name__ == "__main__":
    # 测试生成
    print("🚒 生成消防喷头 BOM...")
    print("="*60)
    
    bom_data = generate_spinkler_bom("SPR-2026-001")
    print(json.dumps(bom_data, ensure_ascii=False, indent=2))
