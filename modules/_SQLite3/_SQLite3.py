#  Copyright (c) 2025.
#  702361946@qq.com(https://github.com/702361946)
import sqlite3
from typing import Any

from _get_package import *

log = Log(
    log_sign="SQLite",
    log_output_to_file_path=f"{log_path}SQLite",
    log_output_to_file_mode="w"
)


class SQLite3:
    def __init__(self, db_name: str, auto_commit: bool = True, *, log: Log = log):
        """

        :param db_name:
        :param auto_commit: 自动提交事务,为False时请手动提交事务
        :param log:
        """
        self.log = log
        self.name = db_name
        self.connect = sqlite3.connect(db_name, autocommit=auto_commit)
        self.cursor = self.connect.cursor()

        self.log.info(f"open db {db_name}\\{auto_commit=}")

    def close(self):
        """

        :return:
        """
        self.cursor.close()
        self.connect.close()
        self.log.info(f"close db {self.name}")

    def commit(self):
        """

        :return:
        """
        self.connect.commit()
        self.log.info(f"commit")

    def rollback(self):
        """

        :return:
        """
        self.connect.rollback()
        self.log.info("rollback")

    def execute(self, sql: str, parameters: tuple = None) -> Any:
        """
        执行 SQL 语句
        :param sql: SQL 语句
        :param parameters: 参数
        :return: None
        """
        try:
            if parameters:
                self.cursor.execute(sql, parameters)
            else:
                self.cursor.execute(sql)
            self.log.info(f"execute sql: {sql} with params: {parameters}")
            return True
        except sqlite3.Error as e:
            self.log.error(f"execute sql failed: {sql} with params: {parameters}, error: {e}")
            return False

    def fetch_all(
            self,
            table_name: str,
            columns: str | list[str] = '*',
            other_params: dict = None
    ) -> list[tuple[Any, ...]]:
        """
        查询所有数据
        :param table_name: 表名
        :param columns: 列名，可以是单个列名字符串或列名列表
        :param other_params: 其他参数，如 WHERE 条件
        :return: 查询结果
        """
        try:
            self.log.info(f"fetch all\n{table_name=}\n{columns=}\n{other_params=}")
            # 处理列名
            if isinstance(columns, list):
                columns = ', '.join(columns)

            # 构造 SQL 语句
            sql = f"SELECT {columns} FROM {table_name}"

            # 添加其他参数
            params = []
            if other_params:
                conditions = []
                for key, value in other_params.items():
                    conditions.append(f"{key} = ?")
                    params.append(value)
                sql += f" WHERE {' AND '.join(conditions)}"

            # 执行查询
            self.cursor.execute(sql, tuple(params) if params else None)
            rows = self.cursor.fetchall()

            self.log.debug(f"{rows=}")

            return rows
        except sqlite3.Error as e:
            self.log.error(e)
            return []

    def fetch_one(
            self,
            table_name: str,
            columns: str | list[str] = '*',
            other_params: dict | None = None
    ) -> tuple[Any, ...] | None:
        """
        查询单条数据
        :param table_name: 表名
        :param columns: 列名，可以是单个列名字符串或列名列表
        :param other_params: 其他参数，如 WHERE 条件
        :return: 查询结果（单条数据）或 None
        """
        try:
            self.log.info(f"fetch one\n{table_name=}\n{columns=}\n{other_params=}")
            # 处理列名
            if isinstance(columns, list):
                columns = ', '.join(columns)

            # 构造 SQL 语句
            sql = f"SELECT {columns} FROM {table_name}"

            # 添加其他参数
            params = []
            if other_params:
                conditions = []
                for key, value in other_params.items():
                    conditions.append(f"{key} = ?")
                    params.append(value)
                sql += f" WHERE {' AND '.join(conditions)}"

            # 执行查询
            self.cursor.execute(sql, tuple(params) if params else None)
            row = self.cursor.fetchone()

            self.log.debug(f"{row=}")

            return row
        except sqlite3.Error as e:
            self.log.error(e)
            return None

    def create_table(self, table_name: str, columns: tuple[str, ...]):
        """
        创建表
        :param table_name: 表名
        :param columns: 列定义
        :return: None
        """
        if not isinstance(columns, tuple):
            columns = tuple(columns,)

        sql = f"CREATE TABLE IF NOT EXISTS {table_name} {columns}"
        self.execute(sql)
        self.log.info(f"create table {table_name} with columns: {columns}")

    def delete_table(self, table_name: str) -> bool:
        """
        删除表
        :param table_name: 表名
        :return: None
        """
        try:
            self.log.info(f"delete table {table_name}")
            # 构造 SQL 语句
            sql = "DROP TABLE IF EXISTS ?"

            # 执行 SQL 语句
            self.execute(sql, (table_name,))
            return True
        except sqlite3.Error as e:
            self.log.error(f"error: {e}")
            return False

    def insert(self, table_name: str, data: dict):
        """
        插入数据
        :param table_name: 表名
        :param data: 数据字典
        :return: None
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))

        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.execute(sql, tuple(data.values()))
        self.log.info(f"insert data into table {table_name}: {data}")

    def update(
            self,
            table_name: str,
            columns: str | list[str],
            data: Any | list[Any],
            condition: str = None
    ) -> bool:
        """
        更新数据
        :param table_name: 表名
        :param columns: 列名，可以是单个列名字符串或列名列表
        :param data: 数据，可以是单个值或值列表
        :param condition: 更新条件，可选
        """
        try:
            self.log.info(f"update\n{table_name=}\n{columns=}\n{data=}")
            # 处理列名和数据
            if isinstance(columns, str):
                columns = [columns]
                data = [data]

            # 构造 SET 子句
            set_clause = ', '.join([f"{col} = ?" for col in columns])

            # 构造 SQL 语句
            sql = f"UPDATE {table_name} SET {set_clause}"

            # 添加条件
            if condition:
                sql += f" WHERE {condition}"

            # 执行 SQL 语句
            self.cursor.execute(sql, tuple(data))
            return True
        except sqlite3.Error as e:
            self.log.error(e)
            return False

    def delete(self, table_name: str, condition_column: str, condition_value: Any) -> bool:
        """
        删除数据
        :param table_name: 表名
        :param condition_column: 条件列名
        :param condition_value: 条件值
        :return: None
        """
        try:
            self.log.info(f"{table_name=}\\{condition_column=}\\{condition_value=}")
            # 构造 SQL 语句
            sql = f"DELETE FROM {table_name} WHERE {condition_column} = ?"

            # 执行 SQL 语句
            self.cursor.execute(sql, (condition_value,))

            # 提交事务
            self.connect.commit()
            return True
        except sqlite3.Error as e:
            self.log.error(e)
            return False

    def __del__(self):
        """

        :return:
        """
        try:
            self.close()
        except Exception as e:
            self.log.error(e)
