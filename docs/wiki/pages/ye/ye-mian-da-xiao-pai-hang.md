---
id: ye-mian-da-xiao-pai-hang
type: list
label: 页面大小排行
aliases: [内容量排行, 页面内容排行, page size ranking]
tags: [索引, 统计]
description: 按正文长度（prose_chars）排序的词条页面排行，反映各页面内容量的分布
quality: standard
---
## 简介

本页按正文长度（prose_chars）聚合展示各词条。正文长度反映页面的信息密度和完整度，是衡量内容充实程度的重要指标。

## 页面大小排行 Top 50

::: query
sort: prose_chars
order: desc
limit: 50
display: table
fields: [label, type, quality, prose_chars, pn_count, h2_count]
field_labels:
  label: 页面
  type: 类型
  quality: 质量
  prose_chars: 正文长度
  pn_count: PN 引注
  h2_count: 小节数
title: 内容量最大 Top 50
:::

## 最短页面 Top 30

::: query
sort: prose_chars
order: asc
limit: 30
display: table
fields: [label, type, quality, prose_chars, pn_count]
field_labels:
  label: 页面
  type: 类型
  quality: 质量
  prose_chars: 正文长度
  pn_count: PN 引注
title: 最短页面 Top 30
:::

## 概念（concept）

::: query
type: concept
sort: prose_chars
order: desc
limit: 20
display: table
fields: [label, quality, prose_chars, pn_count]
field_labels:
  label: 概念
  quality: 质量
  prose_chars: 正文长度
  pn_count: PN 引注
title: 概念页面大小 Top 20
:::

## 人物（person）

::: query
type: person
sort: prose_chars
order: desc
limit: 20
display: table
fields: [label, quality, prose_chars, pn_count]
field_labels:
  label: 人物
  quality: 质量
  prose_chars: 正文长度
  pn_count: PN 引注
title: 人物页面大小 Top 20
:::

## 地点（place）

::: query
type: place
sort: prose_chars
order: desc
limit: 20
display: table
fields: [label, quality, prose_chars, pn_count]
field_labels:
  label: 地点
  quality: 质量
  prose_chars: 正文长度
  pn_count: PN 引注
title: 地点页面大小 Top 20
:::

## 物种（species）

::: query
type: species
sort: prose_chars
order: desc
limit: 20
display: table
fields: [label, quality, prose_chars, pn_count]
field_labels:
  label: 物种
  quality: 质量
  prose_chars: 正文长度
  pn_count: PN 引注
title: 物种页面大小 Top 20
:::

## 历史事件（event）

::: query
type: event
sort: prose_chars
order: desc
limit: 20
display: table
fields: [label, quality, prose_chars, pn_count]
field_labels:
  label: 事件
  quality: 质量
  prose_chars: 正文长度
  pn_count: PN 引注
title: 事件页面大小 Top 20
:::
