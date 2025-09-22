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


class SQLite:
    def __init__(self, db_name: str, auto_commit: bool = True, *, log: Log = log):
        """
        初始化数据库连接

        :param db_name: 数据库文件名
        :param auto_commit: 自动提交事务,为False时请手动提交事务
        :param log:
        """
        self.log = log

        self.log.info(f"open db {db_name}\\{auto_commit=}")
        self.name = db_name
        self.connect = sqlite3.connect(db_name, autocommit=auto_commit)
        self.cursor = self.connect.cursor()

    def close(self):
        """
        关闭数据库连接
        """
        self.log.info(f"close db {self.name}")
        self.cursor.close()
        self.connect.close()

    def commit(self):
        """
        提交事务
        """
        self.log.info(f"commit")
        self.connect.commit()

    def rollback(self):
        """
        回滚事务
        """
        self.log.info("rollback")
        self.connect.rollback()

    def execute(self, sql: str, parameters: tuple = None) -> Any:
        """
        执行 SQL 语句

        :param sql: SQL 语句
        :param parameters: 参数
        :return: 执行结果
        """
        self.log.debug(f"execute\nsql: {sql}\nparams: {parameters}")
        try:
            if parameters:
                self.cursor.execute(sql, parameters)
            else:
                self.cursor.execute(sql)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            self.log.error(f"{'-' * 25}\n\n\n\nERROR:{e}\n\n\n\n{'-' * 25}")
            return False

    def create_table(self, table_name: str, columns: dict) -> bool:
        """
        创建表

        :param table_name: 表名
        :param columns: 列定义，键为列名，值为列类型
        :return: 是否成功
        """
        column_defs = ', '.join([f"{col} {col_type}" for col, col_type in columns.items()])
        sql = f"CREATE TABLE {table_name} ({column_defs});"
        return self.execute(sql) is not False

    def select(self, table_name: str, columns: list = None) -> list:
        """
        查询数据

        :param table_name: 表名
        :param columns: 查询的列名列表，为空时查询所有列
        :return: 查询结果
        """
        if columns:
            column_defs = ', '.join(columns)
        else:
            column_defs = '*'
        sql = f"SELECT {column_defs} FROM {table_name};"
        return self.execute(sql)

    def insert(self, table_name: str, data: dict) -> bool:
        """
        插入数据

        :param table_name: 表名
        :param data: 插入的数据，键为列名，值为列值
        :return: 是否成功
        """
        columns = ', '.join(data.keys())
        values = tuple(data.values())
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({', '.join(['?'] * len(values))});"
        return self.execute(sql, values) is not False

    def update(self, table_name: str, data: dict, condition: str) -> bool:
        """
        更新数据

        :param table_name: 表名
        :param data: 更新的数据，键为列名，值为列值
        :param condition: 更新条件
        :return: 是否成功
        """
        column_defs = ', '.join([f"{col} = ?" for col in data.keys()])
        values = tuple(data.values())
        sql = f"UPDATE {table_name} SET {column_defs} WHERE {condition};"
        return self.execute(sql, values) is not False

    def delete(
            self,
            table_name: str,
            condition: dict[str, str] | str,
            parameters: Any | list[Any] | tuple[Any, ...] = None
    ) -> bool:
        """
        删除数据

        :param table_name: 表名
        :param condition: 删除条件, 当type为str时直接拼接, 为dict时为'{key} {value} ?', 值为符号
        :param parameters: 参数
        :return: 是否成功
        """
        # parameters type is tuple
        if parameters is not None:
            if isinstance(parameters, list):
                parameters = tuple(parameters)
            elif not isinstance(parameters, tuple):
                parameters = (parameters,)

        sql_condition = condition
        if not isinstance(condition, str):
            if isinstance(condition, dict):
                t = []
                for k, v in condition.items():
                    t.append(f'{k} {v} ?')

                sql_condition = " AND ".join(t)
            else:
                self.log.error("condition type not str or dict")
                return False

        sql = f"DELETE FROM {table_name} WHERE {sql_condition};"

        if parameters is None:
            return self.execute(sql) is not False

        return self.execute(sql, parameters) is not False

    def drop_table(self, table_name: str) -> bool:
        """
        删除表

        :param table_name: 表名
        :return: 是否成功
        """
        sql = f"DROP TABLE {table_name};"
        return self.execute(sql) is not False

    def alter_table(
            self,
            table_name: str,
            action: str,
            column_name: str = None,
            constraint: str = None,
            new_name: str = None
    ) -> bool:
        """
        action=ADD COLUMN: 要求column_name不为None
        action=DROP COLUMN: 要求column_name不为None
        action=RENAME COLUMN: 要求column_name&new_name不为None
        action=RENAME TABLE: 要求new_name不为None
        action=ADD CONSTRAINT: 要求constraint不为None

        :param table_name:
        :param action: ADD COLUMN, DROP COLUMN, RENAME COLUMN, RENAME TABLE, ADD CONSTRAINT
        :param column_name:
        :param constraint: 列类型,在添加列约束(ADD CONSTRAINT)时需要
        :param new_name: 重命名列或表时,作为列或表的新名称
        :return:
        """
        sql = ""
        self.log.info(f"action is {action}")
        match action.upper():
            case "ADD COLUMN":
                if column_name is None:
                    self.log.error("Column_name is None")
                    return False

                sql = f"ALTER TABLE {table_name} ADD COLUMN {column_name}"
                if constraint is not None:
                    sql += f" {constraint}"
                sql += ";"

            case "DROP COLUMN":
                if column_name is None:
                    self.log.error("Column_name is None")
                    return False

                sql = f"ALTER TABLE {table_name} DROP COLUMN {column_name};"

            case "RENAME COLUMN":
                if column_name is None or new_name is None:
                    self.log.error("Column_name or/and new_name is None")
                    return False

                sql = f"ALTER TABLE {table_name} RENAME COLUMN {column_name} TO {new_name};"

            case "RENAME TABLE":
                if new_name is None:
                    self.log.error("New_name is None")
                    return False

                sql = f"ALTER TABLE {table_name} RENAME TO {new_name};"

            case "ADD CONSTRAINT":
                if constraint is None:
                    self.log.error("Constraint is None")
                    return False

                sql = f"ALTER TABLE {table_name} ADD CONSTRAINT {constraint};"

            case _:
                self.log.error(f"no action:{action}")
                return False

        return self.execute(sql) is not False

    def create_index(self, index_name: str, table_name: str, column_name: str) -> bool:
        """
        创建索引

        :param index_name: 索引名
        :param table_name: 表名
        :param column_name: 列名
        :return: 是否成功
        """
        sql = f"CREATE INDEX {index_name} ON {table_name} ({column_name});"
        return self.execute(sql) is not False

    def drop_index(self, index_name: str) -> bool:
        """
        删除索引

        :param index_name: 索引名
        :return: 是否成功
        """
        sql = f"DROP INDEX {index_name};"
        return self.execute(sql) is not False

    def pragma(self, command: str) -> list:
        """
        查询数据库元信息

        :param command: PRAGMA 命令
        :return: 查询结果
        """
        sql = f"PRAGMA {command};"
        return self.execute(sql)

    def create_view(self, view_name: str, select_statement: str) -> bool:
        """
        创建视图

        :param view_name: 视图名
        :param select_statement: SELECT 语句
        :return: 是否成功
        """
        sql = f"CREATE VIEW {view_name} AS {select_statement};"
        return self.execute(sql) is not False

    def drop_view(self, view_name: str) -> bool:
        """
        删除视图

        :param view_name: 视图名
        :return: 是否成功
        """
        sql = f"DROP VIEW {view_name};"
        return self.execute(sql) is not False

    def create_trigger(self, trigger_name: str, event: str, table_name: str, when: str, actions: str) -> bool:
        """
        创建触发器

        :param trigger_name: 触发器名
        :param event: 事件，如 INSERT
        :param table_name: 表名
        :param when: 触发时机，如 AFTER
        :param actions: 触发动作
        :return: 是否成功
        """
        sql = f"CREATE TRIGGER {trigger_name} {when} {event} ON {table_name} BEGIN {actions} END;"
        return self.execute(sql) is not False

    def drop_trigger(self, trigger_name: str) -> bool:
        """
        删除触发器

        :param trigger_name: 触发器名
        :return: 是否成功
        """
        sql = f"DROP TRIGGER {trigger_name};"
        return self.execute(sql) is not False

    def attach_database(self, db_file: str, alias: str) -> bool:
        """
        附加数据库

        :param db_file: 数据库文件名
        :param alias: 数据库别名
        :return: 是否成功
        """
        sql = f"ATTACH DATABASE '{db_file}' AS {alias};"
        return self.execute(sql) is not False

    def detach_database(self, alias: str) -> bool:
        """
        分离数据库

        :param alias: 数据库别名
        :return: 是否成功
        """
        sql = f"DETACH DATABASE {alias};"
        return self.execute(sql) is not False

    def analyze(self, table_name: str) -> bool:
        """
        分析数据库

        :param table_name: 表名
        :return: 是否成功
        """
        sql = f"ANALYZE {table_name};"
        return self.execute(sql) is not False

    def vacuum(self) -> bool:
        """
        优化数据库

        :return: 是否成功
        """
        sql = "VACUUM;"
        return self.execute(sql) is not False

    def reindex(self, index_name: str) -> bool:
        """
        重建索引
        :param index_name: 索引名称
        :return: 是否成功
        """
        sql = f"REINDEX {index_name};"
        return self.execute(sql) is not False

    def release(self, savepoint_name: str) -> bool:
        """
        释放保存点

        :param savepoint_name: 保存点名称
        :return: 是否成功
        """
        sql = f"RELEASE {savepoint_name};"
        return self.execute(sql) is not False

    def savepoint(self, savepoint_name: str) -> bool:
        """
        创建保存点

        :param savepoint_name: 保存点名称
        :return: 是否成功
        """
        sql = f"SAVEPOINT {savepoint_name};"
        return self.execute(sql) is not False

    def rollback_to(self, savepoint_name: str) -> bool:
        """
        回滚到保存点

        :param savepoint_name: 保存点名称
        :return: 是否成功
        """
        sql = f"ROLLBACK TO {savepoint_name};"
        return self.execute(sql) is not False
