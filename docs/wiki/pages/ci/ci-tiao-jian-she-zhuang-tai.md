---
id: ci-tiao-jian-she-zhuang-tai
type: list
label: 词条建设状态
aliases: [build status, 建设状态, 条目状态]
tags: [索引, 统计, GROW]
description: 本 wiki 词条建设状态总览，展示各质量等级词条、高引用待提升词条统计
quality: basic
---

## 概览

本页面汇总 wiki 词条的建设状态，用于追踪 GROW 进度。以下查询按不同维度呈现待关注词条。

> 质量等级：stub < basic < standard < featured

## 待提升词条（Stub + Basic）

::: query
quality: stub, basic
sort: total_refs
order: desc
limit: 30
display: table
fields: [label, type, quality, total_refs]
field_labels:
  label: 词条
  type: 类型
  quality: 质量
  total_refs: 引用数
title: Stub & Basic 词条（按引用数降序）
:::

## Standard 词条（可升级至 Featured）

::: query
quality: standard
sort: total_refs
order: desc
limit: 30
display: table
fields: [label, type, quality, total_refs, pn_count]
field_labels:
  label: 词条
  type: 类型
  quality: 质量
  total_refs: 引用数
  pn_count: PN引注数
title: Standard 词条（按引用数降序）
:::

## PN 引注最多词条 Top 30

::: query
sort: pn_count
order: desc
limit: 30
display: table
fields: [label, type, quality, pn_count, wikilink_count]
field_labels:
  label: 词条
  type: 类型
  quality: 质量
  pn_count: PN引注数
  wikilink_count: 内部链接数
title: PN 引注最多 Top 30
:::
