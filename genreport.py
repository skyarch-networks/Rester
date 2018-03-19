#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from docx_simple_service import SimpleDocxService
from docx.shared import Cm, Inches
import json
import os
import glob

docx = SimpleDocxService()


def open_report_json(fname: str):
    fp = open(fname, 'r')
    report = json.load(fp)
    return report


def build_report(report):
    """
    レポートを組み立てます

    :return:
    """
    for case in report["results"]:
        # 文節タイトル表示
        docx.add_head(case["name"], 2)

        with docx.open_text() as text:
            text.add("日付: %s\n" % case["date"])
            text.add("URL: %s\n" % case["url"])
            text.add("テスト結果: %s\n" % case["result"])
            docx.add_head("REQUEST", 3)
            docx.add_head("ヘッダ", 4)
            request = case["request"]
            text.add("メソッド: %s\n" % request["method"])
            with docx.open_text() as text:
                length = len(request["header"])
                table = docx.add_table(row=length, col=2)
                table.autofit = False
                table.style = 'Table Grid'
                set_col_widths(table)

                request_header(request, table)


def request_header(request, table):
    for i, header in enumerate(request["header"]):
        if len(request["header"][header]) > 512:
            value = request["header"][header]
            head = value[0:30]
            tail = value[-30:]
            v = "%s (snip) %s" % (head, tail)
            cell = table.cell(i, 0)
            cell.text = header
            cell = table.cell(i, 1)
            cell.text = v
        #                        text.add("%s:%s\n" % (header, v))

        else:
            cell = table.cell(i, 0)
            cell.text = header
            cell = table.cell(i, 1)
            cell.text = request["header"][header]

def request_header(request, table):
    for i, header in enumerate(request["header"]):
        if len(request["header"][header]) > 512:
            value = request["header"][header]
            head = value[0:30]
            tail = value[-30:]
            v = "%s (snip) %s" % (head, tail)
            cell = table.cell(i, 0)
            cell.text = header
            cell = table.cell(i, 1)
            cell.text = v
        #                        text.add("%s:%s\n" % (header, v))

        else:
            cell = table.cell(i, 0)
            cell.text = header
            cell = table.cell(i, 1)
            cell.text = request["header"][header]


#                        text.add("%s:%s\n" % (header, request["header"][header]))

def set_col_widths(table):
    widths = (Inches(2.0), Inches(4))
    for row in table.rows:
        for idx, width in enumerate(widths):
            row.cells[idx].width = width

if __name__ == "__main__":

    RED = (0xff, 0x00, 0x00)  # (Red, Green, Blue)
    GREEN = (0x00, 0xFF, 0x00)
    #フォント設定
    docx.set_normal_font("ＭＳ明朝", 9)

    # タイトル表示
    docx.add_head(u"テスト結果", 0)

    # 挿絵挿入
    docx.add_picture("report_top.jpg", 3.0)

    reports = glob.glob("result_*")

    for f_name in reports:
        report = open_report_json(f_name)
        docx.add_head(f_name, 1)
        build_report(report)
        docx.add_page_break()






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
