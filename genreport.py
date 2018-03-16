#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from docx_simple_service import SimpleDocxService
import json

def open_report_json(fname: str):
    fp = open(fname, 'r')
    report = json.load(fp)
    return report

if __name__ == "__main__":

    docx = SimpleDocxService()
    RED = (0xff, 0x00, 0x00)  # (Red, Green, Blue)
    GREEN = (0x00, 0xFF, 0x00)

    report = open_report_json("result_Admin_downloadExportFile.json")


    #フォント設定
    docx.set_normal_font("Courier New", 9)

    # タイトル表示
    docx.add_head(u"テスト結果", 0)

    # 挿絵挿入
    docx.add_picture("report_top.jpg", 3.0)

    for case in report["results"]:
        # 文節タイトル表示
        docx.add_head(case["name"], 1)

    # 挿絵挿入
    # docx.add_picture("s_pic.png", 5.0)

    # コードでテキストを生成、docxに入れ込みます。
    # 修飾の例もここで。
    with docx.open_text() as text:
        text.add("\nThis is a my best book.")
        text.add("\nThis is ")
        text.add("a my best").bold()
        text.add(" book.")
        text.add("\nThis is ")
        text.add("a my best").italic()
        text.add(" book.")
        text.add("\nThis is a my best book.").color(*RED)

    # 次の文節
    docx.add_head(u"二個目の話題", 1)

    # コードでテキストを生成、docxに入れ込みます。
    with docx.open_text() as text:
        text.add(u"\nはい、おしまい。")

    # セーブです。
    docx.save("test.docx")

    print("complete.")
