"""
表格渲染工具类
根据 JSON 数据填充 HTML 表格模板
"""
import json
from typing import Dict, List, Any
from bs4 import BeautifulSoup


class TableRenderer:
    """HTML 表格数据填充工具类"""
    
    def __init__(self):
        """初始化表格渲染器"""
        pass
    
    def render_table_from_strings(
        self,
        html_template: str,
        json_data_str: str
    ) -> str:
        """
        从字符串模板和 JSON 字符串填充表格（为 ComfyUI 节点设计）
        
        Args:
            html_template: HTML 模板字符串
            json_data_str: JSON 数据字符串
            
        Returns:
            填充后的 HTML 字符串
        """
        # 解析 JSON 字符串
        json_data = json.loads(json_data_str)
        
        # 填充数据
        filled_html = self._fill_data(html_template, json_data)
        
        return filled_html
    
    def render_table(
        self,
        html_template_path: str,
        json_data_path: str,
        output_path: str = None
    ) -> str:
        """
        根据 JSON 数据填充 HTML 表格模板
        
        Args:
            html_template_path: HTML 模板文件路径
            json_data_path: JSON 数据文件路径
            output_path: 输出文件路径（可选），如果不提供则只返回 HTML 字符串
            
        Returns:
            填充后的 HTML 字符串
        """
        # 读取 HTML 模板
        with open(html_template_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 读取 JSON 数据
        with open(json_data_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        # 填充数据
        filled_html = self._fill_data(html_content, json_data)
        
        # 如果提供了输出路径，保存文件
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(filled_html)
            print(f"✓ 已生成填充数据的 HTML 文件: {output_path}")
        
        return filled_html
    
    def render_table_from_data(
        self,
        html_template_path: str,
        data: List[Dict[str, str]],
        output_path: str = None
    ) -> str:
        """
        根据数据字典填充 HTML 表格模板（不需要 JSON 文件）
        
        Args:
            html_template_path: HTML 模板文件路径
            data: 数据列表，格式同 JSON 中的 data 字段
            output_path: 输出文件路径（可选）
            
        Returns:
            填充后的 HTML 字符串
        """
        # 读取 HTML 模板
        with open(html_template_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 构建 JSON 数据结构
        json_data = {"data": data}
        
        # 填充数据
        filled_html = self._fill_data(html_content, json_data)
        
        # 如果提供了输出路径，保存文件
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(filled_html)
            print(f"✓ 已生成填充数据的 HTML 文件: {output_path}")
        
        return filled_html
    
    def _fill_data(self, html_content: str, json_data: Dict[str, Any]) -> str:
        """
        填充数据到 HTML 模板（内部方法）
        
        Args:
            html_content: HTML 模板内容
            json_data: JSON 数据
            
        Returns:
            填充后的 HTML 字符串
        """
        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 查找 tbody 元素
        tbody = soup.find('tbody')
        if not tbody:
            raise ValueError("HTML 模板中未找到 <tbody> 标签")
        
        # 清空现有的数据行（保留表头行）
        # 找到第一个 tr（表头行）
        header_row = tbody.find('tr')
        if not header_row:
            raise ValueError("HTML 模板中 <tbody> 内未找到表头行")
        
        # 删除所有数据行（保留表头）
        for row in tbody.find_all('tr')[1:]:  # 跳过第一行（表头）
            row.decompose()
        
        # 获取数据
        data_list = json_data.get('data', [])
        
        # 根据 JSON 数据生成新的行
        for item in data_list:
            # 创建新行
            new_row = soup.new_tag('tr')
            new_row['class'] = 'size-cell'
            
            # 添加尺码列
            size_cell = soup.new_tag('td')
            size_cell.string = item.get('size', '')
            new_row.append(size_cell)
            
            # 添加测量数据列
            # 按照表头顺序：后中长、肩宽、胸围、摆围、袖长
            measurements = [
                item.get('back_length', ''),
                item.get('shoulder_width', ''),
                item.get('bust', ''),
                item.get('hem', ''),
                item.get('sleeve_length', '')
            ]
            
            for value in measurements:
                cell = soup.new_tag('td')
                cell.string = str(value)
                new_row.append(cell)
            
            # 将新行添加到 tbody
            tbody.append(new_row)
        
        # 返回格式化后的 HTML
        return soup.prettify()
    
    def validate_json_data(self, json_data_path: str) -> bool:
        """
        验证 JSON 数据格式是否正确
        
        Args:
            json_data_path: JSON 数据文件路径
            
        Returns:
            是否验证通过
        """
        try:
            with open(json_data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 检查是否有 data 字段
            if 'data' not in data:
                print("✗ 错误: JSON 数据缺少 'data' 字段")
                return False
            
            # 检查 data 是否为列表
            if not isinstance(data['data'], list):
                print("✗ 错误: 'data' 字段必须是数组")
                return False
            
            # 检查必需字段
            required_fields = ['size', 'back_length', 'shoulder_width', 'bust', 'hem', 'sleeve_length']
            for i, item in enumerate(data['data']):
                for field in required_fields:
                    if field not in item:
                        print(f"✗ 错误: 第 {i+1} 条数据缺少 '{field}' 字段")
                        return False
            
            print(f"✓ JSON 数据验证通过，共 {len(data['data'])} 条记录")
            return True
            
        except json.JSONDecodeError as e:
            print(f"✗ 错误: JSON 格式错误 - {e}")
            return False
        except Exception as e:
            print(f"✗ 错误: {e}")
            return False


# 使用示例
if __name__ == "__main__":
    import os
    
    # 初始化渲染器
    renderer = TableRenderer()
    
    # 方式 1: 从文件读取模板和数据
    print("\n" + "="*70)
    print("示例 1: 从 HTML 模板和 JSON 数据生成表格")
    print("="*70)
    
    # 获取项目根目录
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    html_template = os.path.join(project_root, "table_template", "style1.html")
    json_data = os.path.join(project_root, "table_template", "style1.json")
    output_file = os.path.join(project_root, "output_table.html")
    
    # 验证 JSON 数据
    if renderer.validate_json_data(json_data):
        # 渲染表格
        result = renderer.render_table(html_template, json_data, output_file)
        print(f"生成的 HTML 文件: {output_file}")
    
    # 方式 2: 直接使用数据字典
    print("\n" + "="*70)
    print("示例 2: 使用数据字典生成表格")
    print("="*70)
    
    custom_data = [
        {
            "size": "XL",
            "back_length": "45",
            "shoulder_width": "38",
            "bust": "104",
            "hem": "100",
            "sleeve_length": "66.6"
        },
        {
            "size": "XXL",
            "back_length": "46",
            "shoulder_width": "39",
            "bust": "108",
            "hem": "104",
            "sleeve_length": "67.8"
        }
    ]
    
    output_file_2 = os.path.join(project_root, "output_table_custom.html")
    result = renderer.render_table_from_data(html_template, custom_data, output_file_2)
    print(f"生成的 HTML 文件: {output_file_2}")
    
    print("\n" + "="*70)
    print("✓ 所有示例运行完成！")
    print("="*70)
