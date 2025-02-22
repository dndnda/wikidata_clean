#!/bin/bash

# 默认下载链接（根据需要修改）
#DEFAULT_URL="https://dumps.wikimedia.org/zhwiki/20250201/zhwiki-20250201-pages-articles-multistream1.xml-p1p187712.bz2"
DEFAULT_URL="https://dumps.wikimedia.org/zhwiki/20250201/zhwiki-20250201-pages-articles-multistream1.xml-p1p187712.bz2"

# 如果传入参数，则使用该参数作为下载链接，否则使用默认链接
if [ -n "$1" ]; then
    DOWNLOAD_URL="$1"
else
    DOWNLOAD_URL="$DEFAULT_URL"
fi

echo "开始从链接下载数据: $DOWNLOAD_URL"

# 使用 wget 下载数据
wget -O data.bz2 "$DOWNLOAD_URL"

