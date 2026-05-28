---
title: size-limit
category: crypto
genre: rsa
difficulty: medium
tags:
  - raw-rsa
  - leaked-d
  - oversized-plaintext
  - size-limit
source: size-limit/size-limit/problem.py
solved_at: 2026-05-29
---

# size-limit

## 問題の要点

- `N`, `e`, `c`, `d` が出力される。
- flag の長さは 131 bytes で、1024-bit modulus より大きい。
- つまり、暗号化は raw RSA でも平文をそのまま保持できない。

## 解き方の知見

1. まず `m = pow(c, d, N)` を計算して residue を得る。
2. これは元の flag ではなく、`flag mod N` に相当する。
3. 元の flag は `m + kN` の形なので、長さや文字種、既知の prefix で候補を絞る。

今回の flag 長は 131 bytes なので、候補 `k` は
`2^(8*130) <= m + kN < 2^(8*131)` で絞れる。
さらに mirror 元の flag format は `TSGLIVE{...}` なので、prefix 範囲に入るものを探す。

見つかった `k` は `15128635`。

```text
TSGLIVE{Tttthhhhhiiiiiiisssss iiiiiiiiiisssss aaaaaaaaaaaaaa tooooooooooooooooooooo looooooooooooooooong fllllaaaaaaaaaaaaaaaaaag!}
```

## 使いどころ

- `d` が漏れている raw RSA 問題
- 平文サイズが modulus を超える問題
- 既知フォーマットがあり、lift で復元する問題

## 連携する知見

- [RSA](../../../insights/rsa.md)
- [RSA relations](../../../relations/rsa.md)

## メモ

この手の問題は「復号できるか」ではなく、「復号結果から元の平文をどう lift するか」が本題になる。
