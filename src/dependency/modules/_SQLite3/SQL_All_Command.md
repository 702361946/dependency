| 语句                     | 效果       | 语句                                                               | v\_type                                                    |
|------------------------|----------|------------------------------------------------------------------|------------------------------------------------------------|
| `CREATE TABLE`         | 创建一个新表   | `CREATE TABLE v1 (v2 INTEGER PRIMARY KEY, v3 TEXT, v4 INTEGER);` | `v1: TABLE_NAME \| v2: INTEGER \| v3: TEXT \| v4: INTEGER` |
| `SELECT`               | 查询数据     | `SELECT * FROM v1;`                                              | `v1: TABLE_NAME`                                           |
| `INSERT INTO`          | 插入数据     | `INSERT INTO v1 (v2, v3) VALUES ('Alice', 30);`                  | `v1: TABLE_NAME \| v2: COLUMN_NAME \| v3: COLUMN_NAME`     |
| `UPDATE`               | 更新数据     | `UPDATE v1 SET v3 = 31 WHERE v2 = 'Alice';`                      | `v1: TABLE_NAME \| v2: COLUMN_NAME \| v3: COLUMN_NAME`     |
| `DELETE FROM`          | 删除数据     | `DELETE FROM v1 WHERE v2 = 'Alice';`                             | `v1: TABLE_NAME \| v2: COLUMN_NAME`                        |
| `DROP TABLE`           | 删除表      | `DROP TABLE v1;`                                                 | `v1: TABLE_NAME`                                           |
| `ALTER TABLE`          | 修改表结构    | `ALTER TABLE v1 ADD COLUMN v2 TEXT;`                             | `v1: TABLE_NAME \| v2: COLUMN_NAME`                        |
| `CREATE INDEX`         | 创建索引     | `CREATE INDEX v1 ON v2 (v3);`                                    | `v1: INDEX_NAME \| v2: TABLE_NAME \| v3: COLUMN_NAME`      |
| `DROP INDEX`           | 删除索引     | `DROP INDEX v1;`                                                 | `v1: INDEX_NAME`                                           |
| `PRAGMA`               | 查询数据库元信息 | `PRAGMA table_info(v1);`                                         | `v1: TABLE_NAME`                                           |
| `CREATE VIEW`          | 创建视图     | `CREATE VIEW v1 AS SELECT * FROM v2;`                            | `v1: VIEW_NAME \| v2: TABLE_NAME`                          |
| `DROP VIEW`            | 删除视图     | `DROP VIEW v1;`                                                  | `v1: VIEW_NAME`                                            |
| `CREATE TRIGGER`       | 创建触发器    | `CREATE TRIGGER v1 AFTER INSERT ON v2 BEGIN SELECT 1; END;`      | `v1: TRIGGER_NAME \| v2: TABLE_NAME`                       |
| `DROP TRIGGER`         | 删除触发器    | `DROP TRIGGER v1;`                                               | `v1: TRIGGER_NAME`                                         |
| `BEGIN TRANSACTION`    | 开始事务     | `BEGIN TRANSACTION;`                                             | `None`                                                     |
| `COMMIT TRANSACTION`   | 提交事务     | `COMMIT TRANSACTION;`                                            | `None`                                                     |
| `ROLLBACK TRANSACTION` | 回滚事务     | `ROLLBACK TRANSACTION;`                                          | `None`                                                     |
| `ATTACH DATABASE`      | 附加数据库    | `ATTACH DATABASE 'v1.db' AS v2;`                                 | `v1: DATABASE_FILE \| v2: DATABASE_ALIAS`                  |
| `DETACH DATABASE`      | 分离数据库    | `DETACH DATABASE v1;`                                            | `v1: DATABASE_ALIAS`                                       |
| `ANALYZE`              | 分析数据库    | `ANALYZE v1;`                                                    | `v1: TABLE_NAME`                                           |
| `VACUUM`               | 优化数据库    | `VACUUM;`                                                        | `None`                                                     |
| `REINDEX`              | 重建索引     | `REINDEX v1;`                                                    | `v1: INDEX_NAME`                                           |
| `RELEASE`              | 释放保存点    | `RELEASE v1;`                                                    | `v1: SAVEPOINT_NAME`                                       |
| `SAVEPOINT`            | 创建保存点    | `SAVEPOINT v1;`                                                  | `v1: SAVEPOINT_NAME`                                       |
| `ROLLBACK TO`          | 回滚到保存点   | `ROLLBACK TO v1;`                                                | `v1: SAVEPOINT_NAME`                                       |
