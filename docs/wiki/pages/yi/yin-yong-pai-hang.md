---
id: yin-yong-pai-hang
type: list
label: 引用排行
aliases: [引用索引, 词条引用排行, ref ranking]
tags: [索引, 引用, 统计]
quality: basic
description: 按引用数统计的本 wiki 词条排行，反映词条间的链接密度和核心度
---

## 简介

本页按引用数（total_refs）聚合展示各词条。引用数反映其他词条页面对该词条的链接频率，是衡量词条核心度的重要指标。引用越高的词条在戴蒙德的论述中越具枢纽地位。

## 跨领域高频词条 Top 50

::: query
sort: total_refs
order: desc
limit: 50
display: table
fields: [label, type, quality, total_refs]
field_labels:
  label: 词条
  type: 类型
  quality: 质量
  total_refs: 引用数
title: 高频词条 Top 50
:::

## 概念（concept）

::: query
type: concept
sort: total_refs
order: desc
limit: 30
display: table
fields: [label, quality, total_refs]
field_labels:
  label: 概念
  quality: 质量
  total_refs: 引用数
title: 高频概念 Top 30
:::

## 人物（person）

::: query
type: person
sort: total_refs
order: desc
limit: 30
display: table
fields: [label, quality, total_refs]
field_labels:
  label: 人物
  quality: 质量
  total_refs: 引用数
title: 高频人物 Top 30
:::

## 地点（place）

::: query
type: place
sort: total_refs
order: desc
limit: 30
display: table
fields: [label, quality, total_refs]
field_labels:
  label: 地点
  quality: 质量
  total_refs: 引用数
title: 高频地点 Top 30
:::

## 物种（species）

::: query
type: species
sort: total_refs
order: desc
limit: 30
display: table
fields: [label, quality, total_refs]
field_labels:
  label: 物种
  quality: 质量
  total_refs: 引用数
title: 高频物种 Top 30
:::

## 历史事件（event）

::: query
type: event
sort: total_refs
order: desc
limit: 30
display: table
fields: [label, quality, total_refs]
field_labels:
  label: 事件
  quality: 质量
  total_refs: 引用数
title: 高频事件 Top 30
:::
