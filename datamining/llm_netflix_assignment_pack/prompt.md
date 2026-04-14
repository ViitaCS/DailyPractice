# Prompt 设计说明

## 一、任务 A：缺失值填补（rating）

### 1. Zero-shot Prompt
```text
你是一个数据预处理助手。请根据以下 Netflix 节目的上下文信息，推断最可能的 age rating（如 TV-MA、TV-14、PG、PG-13、R、TV-PG 等）。

要求：
1. 只能输出一个 rating 标签；
2. 如果信息不足，也必须给出最可能结果；
3. 不要输出解释。

输入：
title: {title}
type: {type}
release_year: {release_year}
listed_in: {listed_in}
description: {description}
```

### 2. Few-shot Prompt
```text
你是一个数据预处理助手，需要根据上下文推断 Netflix 节目的 age rating。

示例1：
title: Example Family Movie
type: Movie
release_year: 2018
listed_in: Children & Family Movies, Comedies
description: A heartwarming family comedy about friendship and school life.
输出：PG

示例2：
title: Example Crime Show
type: TV Show
release_year: 2020
listed_in: Crime TV Shows, TV Dramas
description: Detectives investigate brutal murders involving drugs and gang violence.
输出：TV-MA

现在请判断：
title: {title}
type: {type}
release_year: {release_year}
listed_in: {listed_in}
description: {description}
输出：
```

## 二、任务 B：文本结构化（description -> JSON）

### 1. Zero-shot Prompt
```text
请把下面的 Netflix 节目简介结构化为 JSON，并严格输出 JSON，不要输出其他文字。

字段要求：
- main_theme: 主要主题，字符串
- target_audience: 目标受众，字符串
- mood: 情绪基调，字符串
- risk_tags: 风险标签，字符串列表

文本：
{description}
```

### 2. Few-shot Prompt
```text
你是一个文本结构化助手。请把节目简介提取成 JSON。

示例输入：
A young girl and her dragon friend embark on a magical journey to save their village.

示例输出：
{
  "main_theme": "friendship and adventure",
  "target_audience": "teen and family",
  "mood": "inspiring",
  "risk_tags": []
}

现在请处理下面文本，并严格输出 JSON：
{description}
```

