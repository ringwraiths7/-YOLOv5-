import os
import xml.etree.ElementTree as ET

def convert_xml_to_yolo(input_folder, output_folder):
    """
    将XML格式标注文件转换为YOLO格式的TXT文件
    
    参数:
    input_folder -- 包含XML文件的输入文件夹路径
    output_folder -- 保存TXT文件的输出文件夹路径
    """
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)
    
    # 创建类别映射字典（根据实际类别修改）
    class_mapping = {
        "holothurian": 0,#海参
        "echinus": 1,#海胆
        "scallop": 2,#扇贝
        "starfish": 3#海星
    }
    
    # 遍历输入文件夹中的所有XML文件
    for filename in os.listdir(input_folder):
        if not filename.endswith('.xml'):
            continue
            
        xml_path = os.path.join(input_folder, filename)
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # 获取图像尺寸
        size = root.find('size')
        img_width = int(size.find('width').text)
        img_height = int(size.find('height').text)
        
        # 准备输出TXT文件名
        txt_filename = os.path.splitext(filename)[0] + '.txt'
        txt_path = os.path.join(output_folder, txt_filename)
        
        with open(txt_path, 'w') as txt_file:
            # 遍历所有检测对象
            for obj in root.findall('object'):
                name = obj.find('name').text
                bbox = obj.find('bndbox')
                
                # 提取边界框坐标
                xmin = float(bbox.find('xmin').text)
                ymin = float(bbox.find('ymin').text)
                xmax = float(bbox.find('xmax').text)
                ymax = float(bbox.find('ymax').text)
                
                # 转换为YOLO格式
                x_center = (xmin + xmax) / (2.0 * img_width)
                y_center = (ymin + ymax) / (2.0 * img_height)
                width = (xmax - xmin) / img_width
                height = (ymax - ymin) / img_height
                
                # 获取类别ID
                class_id = class_mapping.get(name)
                if class_id is None:
                    print(f"警告: 在文件 {filename} 中发现未知类别 '{name}'，已跳过")
                    continue
                
                # 写入TXT文件
                txt_file.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")
        
        print(f"转换完成: {filename} -> {txt_filename}")

# 使用示例
if __name__ == "__main__":
    input_folder = "rawdata/test-A-box"  # 替换为你的XML文件夹路径
    output_folder = "mydata/val/labels"  # 替换为输出文件夹路径
    
    convert_xml_to_yolo(input_folder, output_folder)