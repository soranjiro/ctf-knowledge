---
title: Rotten Beef
category: pwn
genre: format-string
difficulty: medium
tags:
  - fsb
  - arbitrary-write
  - percent-n
source: alpacahack:rotten-beef
solved_at: 2026-05-29
---

# Rotten Beef

## 問題の要点

- 入力は `scanf("%11s", buffer)` で 11 byte まで。
- その後 `printf(buffer, &key, &dummy)` として入力が format string になる。
- `key = 0xdead` を `0xbeef` に変えればよい。

## 解き方

第1引数に `&key` が渡っているので、`%1$n` でこれまでに出力した文字数を書き込める。

```text
%48879c%1$n
```

`0xbeef = 48879`。

## 知見

- 入力長が短くても、`printf(user_input, ptr...)` のように都合のよい引数があると `%n` が刺さる。
- format string は leak だけでなく write primitive として見る。

## 連携する知見

- [Pwn](../../../insights/pwn.md)
- [Pwn relations](../../../relations/pwn.md)
