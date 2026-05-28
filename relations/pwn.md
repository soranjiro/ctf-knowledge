# Pwn Relations

Pwn 関連 writeup の index。
個別 offset や payload は writeup に置き、ここでは exploit primitive ごとに探せるようにする。

## 関連 insights

- [Pwn](../insights/pwn.md)

## 事例一覧

- [Integer Writer](../writeup/alphahack/2025-w49/1205_integer-writer.md): 負 index の OOB write で return address を直接 ret2win に変える。
- [simpleoverflow](../writeup/alphahack/2025-w49/1206_simpleoverflow.md): 小さい stack overflow で隣接する `is_admin` を書き換える。
- [login-bonus](../writeup/alphahack/2025-w51/1217_login-bonus.md): 長さ制限なし `scanf` で global の `secret` を上書きし、`strcmp` を通す。
- [alloc-101](../writeup/alphahack/2025-w51/1219_alloc-101.md): free 後に pointer を NULL 化しない UAF。同サイズ再確保で flag chunk を読む。
- [Rotten Beef](../writeup/alphahack/2025-w52/1223_rotten-beef.md): format string の `%n` で `key` を `0xbeef` にする。
- [simpleoverwrite](../writeup/alphahack/2025-w52/1227_simpleoverwrite.md): stack BOF で return address を `win` に向ける。

## 比較観点

- stack overflow: `simpleoverflow`, `simpleoverwrite`
- OOB write: `Integer Writer`
- global overwrite: `login-bonus`
- heap UAF: `alloc-101`
- format string write: `Rotten Beef`
