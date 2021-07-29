import sqlite3
import traceback


class DbConfig:
    """
    从数据库中获取企业微信通信的相关参数
    """

    def __init__(self, table, db_path):
        self.table = table
        self.db_path = db_path

    def initial_table(self):
        """
        初始化数据以及库表
        :return:
        """
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("""
            create table if not exists gmzz
            (
                chapter_name text,
                chapter_content text,
                last_chapter text,
                update_time bigint
            );
        """)
        conn.commit()
        conn.close()

    def get_params(self, *params):
        """
        自定义获取参数
        :param params:list: access_token、crop_id、crop_secret、token、enconding_aes_key
        :return:
        """
        try:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            cursor = conn.cursor()
            sql = "select {} from {} ".format(",".join(list(params[0])), self.table)
            rtn = cursor.execute(sql)
            result = list(rtn)
            conn.close()
            return result
        except Exception as e:
            traceback.print_exc()

    def simple_query(self, sql):
        try:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            cursor = conn.cursor()
            rtn = cursor.execute(sql)
            conn.close()
            return list(rtn)
        except Exception as e:
            traceback.print_exc()

    def add_one(self,fields, values):
        try:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            cursor = conn.cursor()
            sql = "insert into {} ({}) values ('{}')".format(self.table, ",".join(fields), ",".join(values))
            print(sql)
            rtn = cursor.execute(sql)
            conn.commit()
            conn.close()
            return rtn
        except Exception as e:
            traceback.print_exc()

    def update_one(self, field_name, update_value):
        """
        更新某个字段
        :param field_name: 字段名称
        :param update_value: 跟新值
        :return:
        """
        try:
            sql = "update {table} set {field_name} = '{update_value}'".format(
                table=self.table,
                field_name=field_name,
                update_value=update_value
            )
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            conn.close()
        except Exception as e:
            traceback.print_exc()


if __name__ == '__main__':
    pass
