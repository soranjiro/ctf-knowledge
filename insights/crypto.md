# Crypto

RSA 以外の crypto は、まず「何が数学的に保存されているか」を見る。
文字列が整数、素因数、剰余、XOR、乱数列、置換のどれとして表現されているかを分類すると、戻し方が見えやすい。

## 初動

- encoding を見る: bytes-to-long, hex, base64, prime exponent, ord/chr。
- 演算を見る: XOR, 加算, 乗算, mod, pow, shuffle, PRNG。
- 独立な成分に分解できないかを見る: 素因数ごとの指数、文字ごとの変換、ブロックごとの処理。
- 既知 plaintext や flag format を制約として使う。

## 壊れやすい部分

- **素因数の指数に情報を埋める**: factorization すれば各文字の code point がそのまま出る。
- **XOR の使い回し**: 同じ key や短い key は既知 prefix で戻せる。
- **独自 encoding**: 見た目が巨大整数でも、構造が可逆なら暗号ではない。
- **PRNG/LCG**: 状態更新が線形なら、出力差分や連立方程式で戻せる。

## 考え方

1. 暗号か encoding かを分ける。
2. 可逆な操作なら逆順に戻す。
3. 巨大整数なら factorization、剰余、bit length、桁数を確認する。
4. 乱数が絡む場合は seed/state/update のどれが漏れているかを見る。

## 実戦メモ

- `prod(p_i ** ord(flag[i]))` のような形は、素因数分解がそのまま decode。
- crypto 問でも、flag format と printable 制約は solver の強い条件になる。
