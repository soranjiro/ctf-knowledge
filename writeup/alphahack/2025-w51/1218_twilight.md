---
title: Twilight
category: rev
genre: flag-transform
difficulty: medium
tags:
  - function-pointer
  - inverse-transform
  - index-dependent
source: alpacahack:twilight
solved_at: 2026-05-29
---

# Twilight

## 問題の要点

- 入力 flag の各文字に対して、`i % 2` で関数ポインタを切り替える。
- 偶数/奇数で `ch + i` と `ch ^ i` のような変換をして、出力列と比較する。

## 解き方

デコンパイルして関数 `a`, `b` の意味を読む。

```c
int a(int ch, int i) { return ch + i; }
int b(int ch, int i) { return ch ^ i; }
```

出力値 `out[i]` から逆変換する。

```python
if i % 2 == 0:
    ch = out[i] - i
else:
    ch = out[i] ^ i
```

## 得られた flag

```text
Alpaca{AlpacaHack_in_Wonderland}
```

## 知見

- 関数ポインタを使っていても、呼び出し先の候補が少なければ「どの index でどの関数か」を表にする。
- `+`, `^` のような可逆な1文字変換は、出力列から直接戻せる。

## 連携する知見

- [Rev](../../../insights/rev.md)
- [Rev relations](../../../relations/rev.md)
