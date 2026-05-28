---
title: Fully Padded RSA
category: crypto
genre: rsa
difficulty: hard
tags:
  - common-modulus
  - small-root
  - coppersmith
  - deterministic-padding
source: alpacahack:fully-padded-rsa
solved_at: 2026-05-29
---

# Fully Padded RSA

## 問題の要点

- 同じ modulus `n` と同じ padded message に対して、異なる指数 `e1 = 65517`, `e2 = 65577` で暗号化した `c1`, `c2` が与えられる。
- `gcd(e1, e2) = 3` なので、common modulus attack をそのまま使っても `m` ではなく `m^3 mod n` が得られる。
- padding はランダムではなく、上位側がおおむね `n` 由来で、下位側に短い flag が入る形。

## 解き方

1. 拡張 Euclid で `s, t` を取り、`c1^s * c2^t mod n = m^3 mod n` を得る。
2. flag 長を仮定し、上位既知部分を `prefix = (n >> (8 * len)) << (8 * len)` と置く。
3. `m = prefix + x` と見て、`(prefix + x)^3 - m3 == 0 mod n` の小さい根 `x` を探す。
4. `x < n^(1/3)` に収まるので Coppersmith small roots が使える。

## 使う形

```python
g, s, t = xgcd(e1, e2)
m3 = pow(c1, s, n) * pow(c2, t, n) % n

for flag_len in range(len("Alpaca{}"), 41):
    shift = flag_len * 8
    prefix = (n >> shift) << shift
    # find small root x of (prefix + x)^g - m3 mod n
```

## 得られた flag

```text
Alpaca{p4dd1n6_mu57_u53_r4nd0m_v41u3s}
```

## 知見

- common modulus attack で指数の gcd が 1 でない場合、`m^g` が残る。
- padding が deterministic で未知部分が小さいなら、`m^g` から small root に持ち込める。
- 「RSA の padding」は単に埋めれば安全ではなく、乱数性と検証不能性が重要。

## 連携する知見

- [RSA](../../../insights/rsa.md)
- [RSA relations](../../../relations/rsa.md)
