# RSA

RSA 系の問題を見るときは、まず「普通の RSA と何が違うか」を探す。
CTF では実装やパラメータがわざと壊されていることが多く、鍵長そのものよりも、平文、素数、指数、padding、pow 実装、複数暗号文の関係が攻撃面になる。

## 基本計算

- 通常は `n = p*q`, `phi = (p-1)(q-1)`, `d = e^-1 mod phi`, `m = c^d mod n`。
- modulus が素数 `p` だけなら `phi = p - 1` で復号できる。
- `p` と `q` に関係式があるなら、まず `n` をその関係式に代入して factorization できないか見る。
- `pow(c, d, n)` の結果は常に `m mod n`。元の平文が `n` 以上なら、長さや prefix で `m + k*n` を lift する必要がある。

## 壊れやすい部分

- **padding が deterministic**: 既知部分が大きく未知部分が小さいと Coppersmith/small roots に落ちる。
- **同じ modulus の再利用**: 異なる指数で同じ平文を暗号化すると common modulus attack が使える。
- **指数の gcd が 1 でない**: `m` ではなく `m^g` が得られる。未知部分が小さいなら small root に続く。
- **関連素数**: `q = 2p + 1` などは `n` から二次方程式で復元できる。
- **指数に線形関係がある**: 複数の `m^e` から指数の一次結合を作り、`m^1` に戻せることがある。
- **自作 pow**: 乗算と加算、mod の位置、初期値が壊れると、RSA ではなく線形合同や別演算になる。

## 考え方

1. 与えられた値を分類する: `n`, `e`, `c`, `d`, `p`, `q`, 複数 ciphertext, 実装コード。
2. `n` の構造を見る: 素数1個、関連素数、再利用、サイズ不足。
3. 平文サイズを見る: `bytes_to_long(flag)` が `n` を超えないか。
4. padding を見る: ランダムか、既知 prefix/suffix があるか、未知部分が小さいか。
5. 複数暗号文の関係を見る: 同じ `m`、同じ `n`、指数の gcd、指数更新式。
6. 実装を読む: `pow` 相当が本当に累乗か、mod inverse の modulus は正しいか。

## 代表的な攻撃の形

- `d` leak: `pow(c, d, n)`。ただし平文が大きい場合は residue lifting。
- one-prime RSA: `d = inverse(e, p-1)`。
- related primes: `n = p(2p+1)` などを方程式化。
- common modulus: `s*e1 + t*e2 = g` から `m^g` を得る。
- Coppersmith: `m = known + x` で `x` が十分小さいとき小さい根を探す。
- exponent relation: `c_i = m^{e_i}` の比や冪で、未知指数を消し、同じ base の別冪を得る。

## 実戦メモ

- RSA 問は Sage/Python で式をそのまま試しやすい。まず小さい式に落としてから solver を使う。
- flag format や長さ制約は攻撃の一部。暗号の外側の制約も必ず使う。
- 「安全そうな名前」の関数、例えば `my_pow` や `safe_prime` は名前ではなく式で確認する。
