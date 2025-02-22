## 数据清洗步骤

1. 使用wikiextractor提取出raw data中的文本，输出格式为json

2. 遍历每条数据，做如下清洗：

   - 统一使用中文标点符号，如将`,`替换为`，`
   - 由于原文本中简体中文和繁体中文夹杂，所以统一转化成简体中文
   - 去除特殊字符和某些乱码字符，只保留中文、英文、数字、基本标点和数学符号
   - 处理语言混杂的格式，删除括号内重复的英文字符。比如，维基百科数据中经常有`信息科学（Information science），旧称情报学`这种格式，我将其清洗为`信息科学，旧称情报学`。
   - 规范化格式：去除多余空格和换行，并且合并连续的标点符号
   - 分句。以`。！？`将文本分成单独的句子，然后删除长度小于5的句子，因为数据中有很多损坏的/无意义的句子，通过删除长度小于5的句子能有效清洗掉这部分数据
   - 将处理后的句子重新组合成文本

   说明：由于wiki数据集中，每条数据都是一篇wiki文章中的内容，因此几乎没有重复数据，所以我省略了数据去重这一步。

## Requirement

- re            # 正则
- zhconv   # 简体繁体中文转换
- json 

## Usage

- 下载数据集：`./download.sh`，默认从[该链接](https://dumps.wikimedia.org/zhwiki/20250201/zhwiki-20250201-pages-articles-multistream1.xml-p1p187712.bz2)下载数据，如果需要使用其他链接， 可以在执行脚本的时候进行指定，如：`./download.sh http://example.com/other-data`
- 使用wikiextractor预处理数据，提取出文本： `wikiextractor --json -o extracted_json data.bz2`
- 执行清洗脚本：`python clean.py`，将前1000条数据清洗结果保存至`cleaned_text`文件
