---
title: cha-ll-enge
category: rev
genre: llvm-ir
difficulty: medium
tags:
  - llvm-ir
  - xor
  - static-data
source: alpacahack:cha-ll-enge
solved_at: 2026-05-29
---

# cha-ll-enge

## 問題の要点

- ELF ではなく LLVM IR が配布される。
- `@__const.main.key` に 50 個の整数配列がある。
- 入力長は 49。各位置で `(input[i] ^ key[i]) ^ key[i+1] == 0` を見る。

## 解き方

式を変形すると `input[i] = key[i] ^ key[i+1]`。

```python
flag = "".join(chr(keys[i] ^ keys[i+1]) for i in range(49))
```

## 知見

- LLVM IR は `load/store/getelementptr/br/icmp` を追えば C の配列アクセスと if に戻せる。
- XOR checker は「比較式が 0 になる条件」を代数的に解くと静的に戻せる。

## 連携する知見

- [Rev](../../../insights/rev.md)
- [Rev relations](../../../relations/rev.md)
