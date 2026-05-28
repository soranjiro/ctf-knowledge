---
title: Integer Writer
category: pwn
genre: out-of-bounds-write
difficulty: hard
tags:
  - stack
  - arbitrary-index
  - return-address
  - mitigation-check
source: integer-writer/main.c
solved_at: 2026-05-29
status: investigated
---

# Integer Writer

## 問題の要点

`pos` を受け取り、`integers[pos]` に `int` を 1 回だけ書ける。

```c
int integers[100], pos;

scanf("%d", &pos);
if (pos >= 100) {
    puts("You're a hacker!");
    return 1;
}
scanf("%d", &integers[pos]);
```

`win()` は `0x4011d6`。

## 調査結果

手元の Linux x86_64 バイナリでは、`pos` は `[rbp-0x1a4]`、
`integers[0]` は `[rbp-0x1a0]` にある。
return address は `[rbp+0x8]` なので、差は `0x1a8 = 424` bytes。
`int` 配列の index にすると `424 / 4 = 106`。

意図解は `pos = 106`、`val = 0x4011d6` で return address の下位 4 bytes を
`win()` に変えることだと思われる。

ただし手元バイナリでは `pos >= 100` により `106` が弾かれる。
負の index は通るが、`integers[0]` より低いアドレス側へ進むため return address には届かない。
Ubuntu 24.04 Docker 上でも `106` は拒否されることを確認した。

## 連携する知見

- [Pwn](../../../insights/pwn.md)
- [Pwn relations](../../../relations/pwn.md)
