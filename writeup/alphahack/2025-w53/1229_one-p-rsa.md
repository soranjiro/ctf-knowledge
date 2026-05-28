---
title: one-p-rsa
category: crypto
genre: rsa
difficulty: easy
tags:
  - one-prime-rsa
  - fermat
  - phi
source: alpacahack:one-p-rsa
solved_at: 2026-05-29
---

# one-p-rsa

## 問題の要点

- 通常の RSA と違い、modulus が `n = p` の1素数だけ。
- `ct = m^e mod p` が与えられる。

## 解き方

素数 `p` に対して `phi(p) = p - 1` なので、`d = e^-1 mod (p - 1)` を計算して復号する。

```python
d = pow(e, -1, p - 1)
m = pow(ct, d, p)
print(long_to_bytes(m))
```

## 得られた flag

```text
Alpaca{which_rsa_do_you_like?}
```

## 知見

- RSA の式は `pq` でなくても、群の位数に対する逆元が取れれば戻せる。
- ただし1素数 modulus は factorization 以前に `phi` が即座に分かるので、秘密鍵が作れてしまう。

## 連携する知見

- [RSA](../../../insights/rsa.md)
- [RSA relations](../../../relations/rsa.md)
