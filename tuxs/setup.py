"""
tuxs - 图像生成工具集
包含 Kimi API 集成、表格渲染和 HTML 截图等功能
"""
from setuptools import setup, find_packages
from pathlib import Path

# 读取 README
this_directory = Path(__file__).parent
long_description = ""
readme_file = this_directory / "README.md"
if readme_file.exists():
    long_description = readme_file.read_text(encoding='utf-8')
else:
    long_description = "tuxs - 图像生成工具集"

setup(
    name="tuxs",
    version="0.1.0",
    author="tuxiansheng",
    author_email="",
    description="图像生成工具集，包含 Kimi API 集成、表格渲染和 HTML 截图等功能",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/tuxs",
    packages=['tuxs', 'tuxs.utils'],
    package_dir={'tuxs': '.'},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "python-dotenv>=0.19.0",
        "beautifulsoup4>=4.9.0",
        "selenium>=4.0.0",
        "Pillow>=8.0.0",
        "numpy>=1.19.0",
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=3.0.0',
        ],
    },
    include_package_data=True,
    package_data={
        'tuxs': [
            'utils/*.md',
        ],
    },
)
