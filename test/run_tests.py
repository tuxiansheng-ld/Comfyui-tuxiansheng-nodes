#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试运行脚本
快速运行所有测试或指定测试
"""
import sys
import os
import argparse

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test.test_kimi_table_to_html import run_tests


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="运行 Kimi Table to HTML 工具测试")
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="详细输出模式"
    )
    parser.add_argument(
        "-i", "--integration",
        action="store_true",
        help="包含集成测试（需要设置 KIMI_API_KEY 环境变量）"
    )
    
    args = parser.parse_args()
    
    # 显示测试信息
    print("=" * 70)
    print("Kimi Table to HTML 工具测试套件")
    print("=" * 70)
    print()
    
    # 显示 Python 环境信息
    print(f"Python 版本: {sys.version}")
    print(f"Python 路径: {sys.executable}")
    
    # 检查是否在 conda 环境中
    conda_env = os.getenv("CONDA_DEFAULT_ENV")
    if conda_env:
        print(f"Conda 环境: {conda_env}")
        if conda_env != "comfyui":
            print(f"⚠️  警告: 当前不在 comfyui 环境中，建议先激活 comfyui 环境")
            print(f"         conda activate comfyui")
    else:
        print("⚠️  提示: 未检测到 conda 环境，建议在 comfyui 环境中运行")
    print()
    
    if args.integration:
        if not os.getenv("KIMI_API_KEY"):
            print("⚠️  警告: 未设置 KIMI_API_KEY 环境变量，集成测试将被跳过")
            print()
    else:
        print("ℹ️  提示: 只运行单元测试，使用 -i 参数包含集成测试")
        print()
    
    # 运行测试
    success = run_tests()
    
    if success:
        print("\n✅ 所有测试通过！")
        return 0
    else:
        print("\n❌ 部分测试失败，请检查上面的错误信息")
        return 1


if __name__ == "__main__":
    sys.exit(main())
