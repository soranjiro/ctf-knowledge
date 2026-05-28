---
title: Useful Machine
category: rev
genre: virtual-machine
difficulty: hard
tags:
  - vm
  - z3
  - bitvector
source: alpacahack:useful-machine
solved_at: 2026-05-29
---

# Useful Machine

## 問題の要点

- 独自 VM の bytecode が与えられる。
- opcode は input, immediate, move, add, mul, xor, not 程度。
- 最終的に `mem[0] == 0` になる入力を探す。

## 解き方

VM を Z3 の BitVec 上でエミュレートする。

```python
mem = [z3.BitVecVal(0, 8) for _ in range(256)]
inp = [z3.BitVec(f"input_{i}", 8) for i in range(40)]

if opcode == 0:
    mem[op1] = inp[input_idx]
elif opcode == 3:
    mem[op1] = mem[op1] + mem[op2]
elif opcode == 5:
    mem[op1] = mem[op1] ^ mem[op2]

s.add(mem[0] == 0)
```

入力命令の数を数えると flag 長は 40。

## 知見

- VM rev は、命令セットが小さいなら「逆算」より「シンボリック実行」の方が速いことがある。
- 8-bit VM は Z3 の `BitVec(8)` と相性がよい。加算・乗算の mod 256 も自然に表現できる。

## 連携する知見

- [Rev](../../../insights/rev.md)
- [Rev relations](../../../relations/rev.md)
