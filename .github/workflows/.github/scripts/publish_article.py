#!/usr/bin/env python3
"""
publish_article.py — 更新 articles.json 并写文章 HTML 文件
"""
import json, os, re

slug    = os.environ.get('SLUG', '')
title   = os.environ.get('TITLE', '')
module  = os.environ.get('MODULE', 'tech')
date    = os.environ.get('DATE', '')
summary = os.environ.get('SUMMARY', '')
tags_raw= os.environ.get('TAGS', '')
content = os.environ.get('CONTENT', '')
cover   = os.environ.get('COVER_IMAGE', '/assets/banner-main.jpg')
token   = os.environ.get('TOKEN', '')

# 解析 tags
tags = [t.strip() for t in tags_raw.split(',') if t.strip()]

# ---- 更新 articles.json ----
json_path = 'data/articles.json'
with open(json_path, 'r', encoding='utf-8') as f:
    articles = json.load(f)

# 检查是否已存在
exists = any(a.get('id') == slug or a.get('slug') == slug for a in articles)

if not exists:
    new_entry = {
        "id": slug, "slug": slug, "title": title,
        "date": date, "module": module,
        "summary": summary, "url": f"/article.html?slug={slug}",
        "cover_image": cover
    }
    if tags: new_entry["tags"] = tags
    if content and not content.startswith('<'):
        new_entry["content"] = content
    articles.insert(0, new_entry)  # 新文章插到最前

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

# ---- 写文章 HTML 文件 ----
html_dir = 'articles'
os.makedirs(html_dir, exist_ok=True)
html_path = f'{html_dir}/{slug}.html'

if content and content.startswith('<'):
    # 传入的是完整 HTML，直接写入
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
elif content:
    # 传入的是纯文本，转成简单段落
    paras = content.replace('\n\n', '</p><p>').replace('\n', '<br>')
    body = f'<div class="article-content"><p>{paras}</p></div>'
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(body)

print(f"Published: {slug}")
