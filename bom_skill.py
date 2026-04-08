#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能工艺 BOM 生成器 - OpenClaw 技能版本
只返回纯 JSON，支持数据库查找或大模型生成
"""

import json
import sys
import os
import re

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bom_generator import generate_bom

# 支持的工艺类型
SUPPORTED_PRODUCTS = [
    "火车车头", "和谐型电力机车", "装配线", "消防水炮车", "消防喷头"
]


def parse_user_input(user_input: str) -> tuple:
    """解析用户输入"""
    # 提取产品名称
    product_name = None
    for name in SUPPORTED_PRODUCTS:
        if name in user_input:
            product_name = name
            break
    
    if not product_name:
        return None, None, None
    
    # 提取产品编码
    code_match = re.search(r'编码 [::]?\s*([A-Z0-9-]+)', user_input)
    product_code = code_match.group(1) if code_match else f"BOM-{int(__import__('time').time()) % 10000000}"
    
    return product_name, product_name, product_code


def generate_bom_by_llm(product_name: str, product_code: str) -> str:
    """
    大模型直接生成 BOM（当数据库未找到时使用）
    
    Args:
        product_name: 产品名称
        product_code: 产品编码
    
    Returns:
        纯 JSON 字符串
    """
    # 这里由大模型实际生成，返回占位
    # 实际使用时调用大模型生成完整 BOM
    return json.dumps({
        "status": "generated_by_llm",
        "product_name": product_name,
        "product_code": product_code,
        "message": "请提供该产品的完整工艺数据"
    }, ensure_ascii=False)


def handle_bom_request(user_input: str) -> str:
    """
    处理用户的 BOM 生成请求
    
    Args:
        user_input: 用户输入的自然语言请求
    
    Returns:
        纯 JSON 字符串（用于入库）
    """
    # 解析用户输入
    product_name, _, product_code = parse_user_input(user_input)
    
    if not product_name:
        # 未找到产品，由大模型生成
        return generate_bom_by_llm("未知产品", "UNKNOWN-001")
    
    # 尝试从数据库生成
    try:
        result = generate_bom(product_name, product_name, product_code)
        return result
    except Exception:
        # 如果生成失败，由大模型生成
        return generate_bom_by_llm(product_name, product_code)


def main():
    """命令行测试"""
    if len(sys.argv) >= 3:
        product_name = sys.argv[1]
        product_code = sys.argv[2]
        
        # 生成 BOM 并输出纯 JSON
        print(generate_bom(product_name, product_name, product_code))
    else:
        print("用法：python bom_skill.py <产品名称> <产品编码>")
        print("示例：python bom_skill.py 火车车头 LOC-2026-001")


if __name__ == "__main__":
    main()
