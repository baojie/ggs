# 枪炮、病菌与钢铁 Wiki

贾雷德·戴蒙德《枪炮、病菌与钢铁：人类社会的命运》知识库，基于谢延光译本。

遵循 [Memex Wiki 宪法](~/memex/CONSTITUTION.md)。本地法律见 [LAW.md](LAW.md)。

## 快速开始

```bash
# 本地预览
bash wiki-daemon.sh start   # http://localhost:1997

# 启动管家
/butler

# 发布
bash wiki/scripts/wiki_commit.sh && git push
```

## 目录结构

```
├── corpus/raw/      校勘底稿（只读）
├── docs/wiki/       wiki 内容与配置
├── data/            中间数据（PN 索引、句子库等）
├── local/           本地定制配置
├── logs/            运行日志
└── ref/             RFC、规范文档
```

## 语料说明

- 底本：谢延光译本（epub）
- 校本：修订版 PDF、v2 epub
- 章末异文以 `> 【校勘·XX】` 标注
