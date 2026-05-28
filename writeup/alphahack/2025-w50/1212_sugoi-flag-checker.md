---
title: Sugoi Flag Checker
category: rev
genre: flag-checker
difficulty: hard
tags:
  - strcmp
  - breakpoint
  - dynamic-analysis
source: alpacahack:sugoi-flag-checker
solved_at: 2026-05-29
---

# Sugoi Flag Checker

## 問題の要点

- 複雑そうに見える ELF の flag checker。
- 実際には最終的に入力文字列と平文 flag 候補が `strcmp` で比較される。

## 解き方

Ghidra で比較箇所を見つけ、`strcmp` 呼び出し直前に breakpoint を置く。

```gdb
b *main+321
r
# dummy input を入れる
# strcmp(s1=input, s2=expected) の s2 を読む
```

`strcmp` の第2引数に平文の期待値が載っていた。

## 得られた flag

```text
Alpaca{m3ccha_rand0m_5b0x_d4yo!}
```

## 知見

- checker が複雑でも、最後の比較が平文なら復号ロジックを全部読む必要はない。
- `strcmp`, `memcmp`, `strncmp` の直前は、動的解析で最優先に見る場所。

## 連携する知見

- [Rev](../../../insights/rev.md)
- [Rev relations](../../../relations/rev.md)
