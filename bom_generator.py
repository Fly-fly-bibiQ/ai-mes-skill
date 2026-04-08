#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能工艺 BOM 生成器 - 精简版
只保留核心 BOM 生成功能，输出纯 JSON 用于入库
"""

import json
import datetime
import random

# ============== 工艺知识库 ==============

PROCESS_KNOWLEDGE = {
    "火车车头": {
        "工艺描述": "火车车头是铁路牵引动力设备，负责为列车提供牵引力和动力。",
        "工艺流程": [
            {
                "operation_code": "OP-001",
                "operation_name": "车体焊接",
                "description": "按照车体图纸进行钢结构焊接。",
                "required_materials": [
                    {"material_code": "MAT-301", "quantity": 15.0, "unit": "TON"},
                    {"material_code": "MAT-302", "quantity": 2.5, "unit": "KG"},
                    {"material_code": "MAT-303", "quantity": 0.8, "unit": "KG"}
                ],
                "required_equipment": ["焊接机器人 KR-2000", "数控切割机"],
                "estimated_time": "16-24 小时",
                "personnel_requirement": "4-6 名焊工",
                "quality_control": "无损检测 (UT/RT)"
            },
            {
                "operation_code": "OP-002",
                "operation_name": "柴油机安装",
                "description": "安装主柴油机及其附属系统。",
                "required_materials": [
                    {"material_code": "MAT-304", "quantity": 1.0, "unit": "SET"},
                    {"material_code": "MAT-305", "quantity": 500.0, "unit": "L"}
                ],
                "required_equipment": ["桥式起重机 50 吨"],
                "estimated_time": "8-12 小时",
                "personnel_requirement": "3-4 名装配技师",
                "quality_control": "扭矩校验"
            }
        ],
        "technical_parameters": {"功率": "3000-4000 kW", "牵引力": "400-500 kN"},
        "quality_standards": {"焊接标准": "GB/T 12469-2009"}
    },
    
    "和谐型电力机车": {
        "工艺描述": "和谐型电力机车是中国铁路使用的交流传动电力机车系列。",
        "工艺流程": [
            {
                "operation_code": "OP-001",
                "operation_name": "车体制造",
                "description": "车体钢结构焊接、涂装和总组装。",
                "required_materials": [
                    {"material_code": "MAT-401", "quantity": 18.0, "unit": "TON"}
                ],
                "required_equipment": ["焊接机器人"],
                "estimated_time": "20-30 小时",
                "personnel_requirement": "6-8 名技工",
                "quality_control": "尺寸检测"
            }
        ],
        "technical_parameters": {"功率": "7200-9600 kW"},
        "quality_standards": {"焊接标准": "GB/T 12469-2009"}
    },
    
    "装配线": {
        "工艺描述": "通用装配生产线。",
        "工艺流程": [
            {
                "operation_code": "OP-001",
                "operation_name": "零件预处理",
                "description": "对零件进行清洗、检测和分类。",
                "required_materials": [
                    {"material_code": "MAT-501", "quantity": 100.0, "unit": "L"}
                ],
                "required_equipment": ["清洗机"],
                "estimated_time": "2-4 小时",
                "personnel_requirement": "2-3 名操作员",
                "quality_control": "外观检查"
            }
        ],
        "technical_parameters": {"节拍时间": "30-60 分钟/件"},
        "quality_standards": {"装配标准": "ISO 9001"}
    },
    
    "消防水炮车": {
        "工艺描述": "消防水炮车是现代化的消防救援装备，集灭火、排烟、照明等功能于一体。",
        "工艺流程": [
            {
                "operation_code": "OP-001",
                "operation_name": "底盘预处理",
                "description": "对特种底盘进行清洗、除锈和防腐处理。",
                "required_materials": [
                    {"material_code": "MAT-F001", "quantity": 1.0, "unit": "SET"},
                    {"material_code": "MAT-F002", "quantity": 50.0, "unit": "L"}
                ],
                "required_equipment": ["喷砂设备", "高压清洗机"],
                "estimated_time": "4-6 小时",
                "personnel_requirement": "2-3 名技工",
                "quality_control": "表面质量检查"
            },
            {
                "operation_code": "OP-002",
                "operation_name": "水罐焊接",
                "description": "焊接消防水罐，确保密封性和结构强度。",
                "required_materials": [
                    {"material_code": "MAT-F004", "quantity": 2.5, "unit": "TON"}
                ],
                "required_equipment": ["焊接机器人"],
                "estimated_time": "8-12 小时",
                "personnel_requirement": "3-4 名焊工",
                "quality_control": "水压试验"
            }
        ],
        "technical_parameters": {"水炮射程": "≥60 米", "水炮流量": "≥40 L/s"},
        "quality_standards": {"整车标准": "GB 7956.1-2014"}
    },
    
    "消防喷头": {
        "工艺描述": "消防喷头是自动喷水灭火系统的末端执行机构，通过热敏元件感知火灾温度，自动开启喷水灭火。",
        "工艺流程": [
            {
                "operation_code": "OP-001",
                "operation_name": "零部件铸造",
                "description": "铸造喷头主体、盖板和框架等零部件。",
                "required_materials": [
                    {"material_code": "MAT-S001", "quantity": 5.0, "unit": "KG"},
                    {"material_code": "MAT-S002", "quantity": 0.5, "unit": "KG"}
                ],
                "required_equipment": ["精密铸造机", "热处理炉"],
                "estimated_time": "6-8 小时",
                "personnel_requirement": "2-3 名技工",
                "quality_control": "尺寸检测"
            },
            {
                "operation_code": "OP-002",
                "operation_name": "热敏元件装配",
                "description": "安装玻璃球或易熔合金热敏元件。",
                "required_materials": [
                    {"material_code": "MAT-S003", "quantity": 100.0, "unit": "PC"},
                    {"material_code": "MAT-S004", "quantity": 50.0, "unit": "PC"}
                ],
                "required_equipment": ["精密装配台", "压力测试仪"],
                "estimated_time": "4-6 小时",
                "personnel_requirement": "2-3 名装配技师",
                "quality_control": "密封性测试"
            }
        ],
        "technical_parameters": {"K 系数": "80 或 115", "工作压力": "0.05-1.2 MPa"},
        "quality_standards": {"产品标准": "GB 5135.1-2019"}
    }
}

# ============== 物料名称映射 ==============

MATERIAL_NAMES = {
    "MAT-301": "低碳钢钢板", "MAT-302": "氩气", "MAT-303": "ER309 不锈钢焊丝",
    "MAT-304": "柴油机 16V280ZJA", "MAT-305": "防冻冷却液",
    "MAT-401": "耐候钢钢板",
    "MAT-501": "工业清洗剂",
    "MAT-F001": "特种底盘", "MAT-F002": "工业清洗剂", "MAT-F004": "不锈钢板 304",
    "MAT-S001": "黄铜棒材 H59", "MAT-S002": "铸造石膏", "MAT-S003": "玻璃球热敏元件", "MAT-S004": "橡胶密封垫片"
}

# ============== 外购件标识 ==============

PURCHASED_PARTS = ["MAT-304", "MAT-307", "MAT-F001", "MAT-F007", "MAT-F010", "MAT-S003", "MAT-S004"]


def generate_bom(keyword: str, product_name: str, product_code: str) -> str:
    """
    生成 BOM 的纯 JSON 字符串（用于入库）
    
    Args:
        keyword: 产品关键词
        product_name: 产品名称
        product_code: 产品编码
    
    Returns:
        纯 JSON 字符串，无任何额外文本
    """
    # 查找工艺知识
    process_info = PROCESS_KNOWLEDGE.get(keyword)
    if not process_info:
        return json.dumps({
            "status": "error",
            "message": f"未找到工艺知识：{keyword}"
        }, ensure_ascii=False)
    
    # 生成 BOM 编码
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    random_suffix = random.randint(1000, 9999)
    bom_code = f"BOM-{timestamp}-{random_suffix}"
    
    # 生成 BOM 主表
    bom_main = {
        "bom_code": bom_code,
        "product_name": product_name,
        "product_code": product_code,
        "process_description": process_info["工艺描述"],
        "technical_parameters": json.dumps(process_info["technical_parameters"], ensure_ascii=False),
        "quality_standards": json.dumps(process_info["quality_standards"], ensure_ascii=False),
        "status": "active",
        "version": "1.0",
        "created_by": "MES_BOM_Generator_v1.0"
    }
    
    # 生成 BOM 明细表
    bom_details = []
    for operation in process_info["工艺流程"]:
        for material in operation["required_materials"]:
            bom_detail = {
                "bom_code": bom_code,
                "operation_code": operation["operation_code"],
                "operation_name": operation["operation_name"],
                "material_code": material["material_code"],
                "material_name": MATERIAL_NAMES.get(material["material_code"], material["material_code"]),
                "quantity": material["quantity"],
                "unit": material["unit"],
                "usage_point": "整工序消耗",
                "is_purchased": material["material_code"] in PURCHASED_PARTS,
                "standard_consumption": material["quantity"],
                "loss_rate": 0.02,
                "effective_date": datetime.datetime.now().date().isoformat(),
                "remark": f"用于{operation['operation_name']}"
            }
            bom_details.append(bom_detail)
    
    # 生成工序信息表
    operations = []
    for idx, operation in enumerate(process_info["工艺流程"], 1):
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
    
    # 组装完整 JSON
    result = {
        "status": "success",
        "bom_code": bom_code,
        "bom_main": bom_main,
        "bom_details": bom_details,
        "operations": operations,
        "summary": summary
    }
    
    # 返回纯 JSON 字符串（无缩进，一行）
    return json.dumps(result, ensure_ascii=False)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) >= 4:
        keyword = sys.argv[1]
        product_name = sys.argv[2]
        product_code = sys.argv[3]
        
        # 输出纯 JSON
        print(generate_bom(keyword, product_name, product_code))
    else:
        print("用法：python bom_generator.py <关键词> <产品名称> <产品编码>")
