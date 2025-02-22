import re
import zhconv  # 处理简繁转换
import os
import json

def convert_to_simplified(text):
    """
    将文本转换为简体中文
    """
    return zhconv.convert(text, 'zh-cn')


def normalize_punctuation(text):
    """
    统一使用中文标点符号
    """
    trans_dict = {
        ',': '，',
        '?': '？',
        '!': '！',
        ':': '：',
        ';': '；',
        '(': '（',
        ')': '）',
        '...': '……'
    }
    for eng_punct, zh_punct in trans_dict.items():
        text = text.replace(eng_punct, zh_punct)
    return text


def clean_text(text):
    """
    清洗文本的函数，适用于数学相关的中文训练数据。
    """
    # 1. 统一使用中文标点符号
    text = normalize_punctuation(text)
    
    # 2. 统一使用简体中文
    text = convert_to_simplified(text)
    
    # 3. 去除特殊字符，保留中文、英文、数字、基本标点和数学符号
    text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9。，！？+\-×÷]', '', text)
    
    # 4. 处理语言混杂，删除括号内重复的英文内容
    text = re.sub(r'（[a-zA-Z\s]+）', '', text)
    text = re.sub(r'([a-zA-Z\s]+)', '', text)
    
    # 5. 规范化格式
    text = re.sub(r'\s+', ' ', text).strip()  # 去除多余空格和换行
    text = re.sub(r'([。，！？])\1+', r'\1', text)  # 连续标点合并
    
    # 6. 分句
    sentences = []
    current_sentence = ""
    for char in text:
        current_sentence += char
        if char in '。！？':
            sentences.append(current_sentence.strip())
            current_sentence = ""
    if current_sentence:
        sentences.append(current_sentence.strip())

    
    # 8. 过滤无意义的内容（长度小于5的句子）
    filtered_sentences = [s for s in sentences if len(s) > 5]
    
    # 9. 重新组合文本
    cleaned_text = ''.join(filtered_sentences)
    
    return cleaned_text


def process_json_object(obj):
    processed_obj = {
        "meta": {
            "url": obj['url'],
            "title": convert_to_simplified(obj['title'])
        },
        "text": clean_text(obj['text'])
    }
    return processed_obj



def read_process_and_write_json(root_folder, output_file, max_count=1000):
    """
    遍历 root_folder 目录下的所有文件，逐行读取 JSON 数据，
    使用 process_json_object() 处理每个 JSON 对象，
    并将处理后的结果写入 output_file 文件。
    
    参数:
        root_folder: 要遍历的根目录
        output_file: 输出文件路径
        max_count: 最多处理的数据条数（默认1000条）
    """
    count = 0  # 数据计数器

    with open(output_file, 'w', encoding='utf-8') as out_f:
        for root, _, files in os.walk(root_folder):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if not line:  # 忽略空行
                                continue
                            try:
                                json_obj = json.loads(line)
                                processed_obj = process_json_object(json_obj)
                                if processed_obj is not None and len(processed_obj['text']) >= 10:
                                    out_f.write(json.dumps(processed_obj, ensure_ascii=False) + '\n')
                                    count += 1
                                    if count >= max_count:
                                        print(f"已处理 {count} 条数据，任务结束。")
                                        return
                            except json.JSONDecodeError as e:
                                print(f"解析文件 {file_path} 中 JSON 数据时出错: {e}")
                except Exception as e:
                    print(f"打开文件 {file_path} 时出错: {e}")




# Example usage
root_directory = "extracted_json"  # Change this to the actual folder path
root_directory = os.path.join(os.getcwd(), 'extracted_json')
read_process_and_write_json(root_directory, 'cleaned_text')


