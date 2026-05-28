---
title: RSA debug?
category: crypto
genre: rsa
difficulty: medium
tags:
  - broken-pow
  - linearization
  - modular-inverse
source: alpacahack:rsa-debug
solved_at: 2026-05-29
---

# RSA debug?

## 問題の要点

- `my_pow(a, n, m)` が通常の modular exponentiation に見える。
- しかし乗算すべき箇所が加算になっている。

```python
if n % 2 != 0:
    result = (result + a) % m
a = (a + a) % m
```

## 解き方

この関数は `a^n mod m` ではなく、double-and-add により `1 + a*n mod m` を計算する。
したがって暗号文は `c = 1 + flag * e mod N`。

```python
m = (c - 1) * inverse(e, N) % N
print(long_to_bytes(m))
```

## 知見

- 暗号コードは名前を信用せず、演算子を見る。
- `pow` 実装の乗算が加算に変わると、指数計算ではなく線形計算になる。

## 連携する知見

- [RSA](../../../insights/rsa.md)
- [RSA relations](../../../relations/rsa.md)
