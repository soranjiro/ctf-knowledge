# RSA Relations

RSA 関連 writeup の index。
ここには細かい計算値ではなく、「どの問題がどの型か」「どの insight を見ればよいか」を置く。

## 関連 insights

- [RSA](../insights/rsa.md)

## 事例一覧

- [size-limit](../writeup/alphahack/2025-w49/1207_size-limit.md): `d` leak だけでは終わらず、平文が `N` より大きいので `m + kN` を長さ/prefix で lift する。
- [Fully Padded RSA](../writeup/alphahack/2025-w50/1208_fully-padded-rsa.md): common modulus で `m^3` を取り、deterministic padding の未知下位 bits を Coppersmith で戻す。
- [Safe Prime](../writeup/alphahack/2025-w50/1213_safe-prime.md): `q = 2p + 1` の関連素数により、`n = 2p^2 + p` を解いて factorization する。
- [RSA debug?](../writeup/alphahack/2025-w51/1221_rsa-debug.md): 自作 pow の乗算が加算になっており、`c = 1 + m*e mod N` の線形合同になる。
- [one-p-rsa](../writeup/alphahack/2025-w53/1229_one-p-rsa.md): modulus が素数1個なので `phi = p - 1` が即分かる。
- [RBG](../writeup/alphahack/2025-w53/1230_rbg.md): LCG で更新される指数の関係から、同じ base の複数冪を組み合わせて `m` を復元する。

## 比較観点

- 平文サイズの問題: `size-limit`
- padding の問題: `Fully Padded RSA`
- 素数生成の問題: `Safe Prime`, `one-p-rsa`
- 実装ミスの問題: `RSA debug?`
- 複数暗号文・指数関係の問題: `Fully Padded RSA`, `RBG`
