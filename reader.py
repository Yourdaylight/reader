# -*- coding: utf-8 -*-
import codecs
import os
import re
import sys

from db_utils import DbConfig


class Reader:

    def __init__(self, book_name, txt_path):
        self.book_name = book_name
        self.txt_path = txt_path
        self.db = DbConfig(self.book_name, "./{}.sqlite3".format(self.book_name))
        self.db.initial_table()  # 初始化数据库，用来存放阅读历史
        self.contents = []
        self.book = self.split_book_chapter()

    def split_book_chapter(self):
        """
        读取文本文件，并将文本按章节划分
        :param txt_path:
        :return:
        """
        book_content = {}
        with codecs.open(self.txt_path, "r", encoding="gbk") as f:
            text = f.read().strip()
            chapters = re.split("\n第", text)
            for chapter in chapters:
                text = chapter.split("\n")
                title = text[0]
                text = "\n".join(text)
                book_content[title] = text
        self.contents = list(book_content.keys())
        return book_content

    def get_index(self, key_name):
        """
        根据书的章节名称，获取前一章与后一章
        :param key_name:
        :return:
        """
        this_index = self.contents.index(key_name)
        last_chapter = self.contents[this_index - 1]
        next_chapter = self.contents[this_index + 1]
        return last_chapter, next_chapter

    def start_read(self, chapter_name=None):
        """
        开始阅读, 章节名称为空，且数据库中没有历史记录时，从第一章开始
        :param chapter_name: 章节名称
        :return:
        """

        last_chapter = self.db.get_params(["last_chapter"])
        # 如果没有历史记录或者指定章节，则是第一次阅读,在数据库中新增
        if not last_chapter:
            self.db.add_one(["last_chapter"], [self.contents[0]])
        if not chapter_name:
            chapter_name = last_chapter[0] if last_chapter else self.contents[0]
        chapter_name = chapter_name[0] if isinstance(chapter_name, tuple) else chapter_name
        read_content = "".join(self.book[chapter_name])
        print(read_content)
        forward = ""
        while forward not in ["n", "b", "q"]:
            forward = input("""
                n、下一章
                b、上一章
                q、退出
            """)

        last_chapter_name, next_chapter_name = self.get_index(chapter_name)
        if forward == "q":
            sys.exit(0)
        # 根据命令选择上一章或者下一章，并更新历史记录
        if forward == "n":
            self.db.update_one("last_chapter", next_chapter_name)
            return next_chapter_name
        if forward == "b":
            self.db.update_one("last_chapter", last_chapter_name)
            return last_chapter_name


if __name__ == '__main__':
    mybook = Reader("gmzz", "test.txt")
    chapter_name = None
    while True:
        os.system('cls')
        chapter_name = mybook.start_read(chapter_name)
