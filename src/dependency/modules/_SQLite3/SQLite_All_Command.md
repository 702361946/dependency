| 命令               | 效果                            | 参格式                       |
|------------------|-------------------------------|---------------------------|
| .archive         | 管理SQL归档                       | `.archive ...`            |
| .auth            | 显示授权回调                        | `.auth on&off`            |
| .backup          | 备份数据库到文件                      | `.backup ?DB? FILE`       |
| .bail            | 出错后停止                         | `.bail on&off`            |
| .cd              | 更改工作目录                        | `.cd DIRECTORY`           |
| .changes         | 显示SQL更改的行数                    | `.changes on&off`         |
| .check           | 检查输出是否匹配                      | `.check GLOB`             |
| .clone           | 克隆数据到新数据库                     | `.clone NEWDB`            |
| .connection      | 打开或关闭辅助数据库连接                  | `.connection [close] [#]` |
| .crnl            | 转换换行符                         | `.crnl on&off`            |
| .databases       | 列出附加数据库的名称和文件                 | `.databases`              |
| .dbconfig        | 列出或更改sqlite3_db_config()选项    | `.dbconfig ?op? ?val?`    |
| .dbinfo          | 显示数据库状态信息                     | `.dbinfo ?DB?`            |
| .dump            | 将数据库内容渲染为SQL                  | `.dump ?OBJECTS?`         |
| .echo            | 开关命令回显                        | `.echo on&off`            |
| .eqp             | 启用或禁用自动EXPLAIN QUERY PLAN     | `.eqp on&off\|full`       |
| .excel           | 以电子表格形式显示下一条命令的输出             | `.excel`                  |
| .exit            | 退出程序                          | `.exit ?CODE?`            |
| .expert          | 建议查询的索引                       | `.expert`                 |
| .explain         | 更改EXPLAIN格式化模式                | `.explain ?on&off\|auto?` |
| .filectrl        | 运行sqlite3_file_control()操作    | `.filectrl CMD ...`       |
| .fullschema      | 显示架构和sqlite_stat表内容           | `.fullschema ?--indent?`  |
| .headers         | 开关标题显示                        | `.headers on&off`         |
| .help            | 显示帮助文本                        | `.help ?-all? ?PATTERN?`  |
| .import          | 从文件导入数据到表                     | `.import FILE TABLE`      |
| .indexes         | 显示索引名称                        | `.indexes ?TABLE?`        |
| .limit           | 显示或更改SQLITE_LIMIT值            | `.limit ?LIMIT? ?VAL?`    |
| .lint            | 报告潜在架构问题                      | `.lint OPTIONS`           |
| .load            | 加载扩展库                         | `.load FILE ?ENTRY?`      |
| .log             | 开关日志                          | `.log FILE\|on&off`       |
| .mode            | 设置输出模式                        | `.mode MODE ?OPTIONS?`    |
| .nonce           | 如果nonce匹配，暂停安全模式              | `.nonce STRING`           |
| .nullvalue       | 替换NULL值的字符串                   | `.nullvalue STRING`       |
| .once            | 下一条SQL命令的输出仅输出到文件             | `.once ?OPTIONS? ?FILE?`  |
| .open            | 关闭现有数据库并重新打开文件                | `.open ?OPTIONS? ?FILE?`  |
| .output          | 将输出发送到文件或标准输出                 | `.output ?FILE?`          |
| .parameter       | 管理SQL参数绑定                     | `.parameter CMD ...`      |
| .print           | 打印字符串                         | `.print STRING...`        |
| .progress        | 每N条指令后调用进度处理器                 | `.progress N`             |
| .prompt          | 替换标准提示符                       | `.prompt MAIN CONTINUE`   |
| .quit            | 停止解释输入流                       | `.quit`                   |
| .read            | 从文件读取输入                       | `.read FILE`              |
| .recover         | 从损坏的数据库中恢复数据                  | `.recover`                |
| .restore         | 从文件恢复数据库内容                    | `.restore ?DB? FILE`      |
| .save            | 将内存数据库写入文件                    | `.save ?OPTIONS? FILE`    |
| .scanstats       | 开关sqlite3_stmt_scanstatus()指标 | `.scanstats on&off\|est`  |
| .schema          | 显示匹配模式的CREATE语句               | `.schema ?PATTERN?`       |
| .separator       | 更改列和行分隔符                      | `.separator COL ?ROW?`    |
| .session         | 创建或控制会话                       | `.session ?NAME? CMD ...` |
| .sha3sum         | 计算数据库内容的SHA3哈希值               | `.sha3sum ...`            |
| .shell           | 在系统shell中运行命令                 | `.shell CMD ARGS...`      |
| .show            | 显示各种设置的当前值                    | `.show`                   |
| .stats           | 显示统计信息或开关统计                   | `.stats ?ARG?`            |
| .system          | 在系统shell中运行命令                 | `.system CMD ARGS...`     |
| .tables          | 列出匹配模式的表名                     | `.tables ?TABLE?`         |
| .timeout         | 尝试打开锁定的表的毫秒数                  | `.timeout MS`             |
| .timer           | 开关SQL定时器                      | `.timer on&off`           |
| .trace           | 输出运行的每条SQL语句                  | `.trace ?OPTIONS?`        |
| .vfsinfo         | 显示顶级VFS的信息                    | `.vfsinfo ?AUX?`          |
| .vfslist         | 列出所有可用的VFS                    | `.vfslist`                |
| .vfsname         | 打印VFS堆栈的名称                    | `.vfsname ?AUX?`          |
| .width           | 设置列输出的最小宽度                    | `.width NUM1 NUM2 ...`    |
| .pragma          | 显示或更改PRAGMA设置                 | `.pragma [PRAGMA_NAME]`   |
| .system          | 在系统shell中运行命令                 | `.system CMD ARGS...`     |
| .testctrl        | 运行测试控制操作                      | `.testctrl CMD ...`       |
| .wal\_checkpoint | 触发WAL检查点                      | `.wal_checkpoint ?DB?`    |
