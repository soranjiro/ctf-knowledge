---
title: Leaked Flag Checker
category: rev
genre: flag-checker
difficulty: easy
tags:
  - xor
  - stack-immediate
  - binary-analysis
source: leaked-flag-checker/challenge
solved_at: 2026-05-29
---

# Leaked Flag Checker

## 問題の要点

ソースでは `xor_flag` が `REDACTED` だが、バイナリには比較対象が残っている。
`main` を逆アセンブルすると、stack 上に即値で比較文字列を作ってから、
入力の各 byte を `0x07` と xor して比較している。

比較対象:

```text
46 6b 77 66 64 66 7c 6b 72 64 6c 7e 7a
```

## 解き方

```python
xor_flag = bytes.fromhex("466b776664667c6b72646c7e7a")
print(bytes(b ^ 7 for b in xor_flag).decode())
```

flag:

```text
Alpaca{lucky}
```

## 連携する知見

- [Rev](../../../insights/rev.md)
- [Rev relations](../../../relations/rev.md)
