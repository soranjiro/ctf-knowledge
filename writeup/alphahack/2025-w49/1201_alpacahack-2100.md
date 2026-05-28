---
title: AlpacaHack 2100
category: misc
genre: welcome
difficulty: welcome
tags:
  - daily-calendar
  - flag-fragments
  - future-month
source: https://alpacahack.com/daily/challenges/alpacahack-2100
solved_at: 2026-05-29
---

# AlpacaHack 2100

## 問題の要点

- Welcome 問題。
- チャレンジページだけでなく、Daily AlpacaHack のカレンダー表示が入力になる。
- `2100-01` の予定トピックに flag 片が隠れている。

## 解き方

`https://alpacahack.com/daily?month=2100-01` を見ると、1/11 から 1/17 に
`Flag` カテゴリの planned topic が並ぶ。

```text
Alpaca{
brought_AGI_
to_humanity...
_yes,_Alpaca
_Gentle_
Intelligence
.}
```

順番に連結して flag は次の通り。

```text
Alpaca{brought_AGI_to_humanity..._yes,_Alpaca_Gentle_Intelligence.}
```

## 連携する知見

- [Misc](../../../insights/misc.md)
- [Misc relations](../../../relations/misc.md)
