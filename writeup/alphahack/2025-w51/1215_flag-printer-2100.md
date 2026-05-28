---
title: Flag Printer 2100
category: rev
genre: anti-wait
difficulty: medium
tags:
  - sleep-skip
  - debugger
  - control-flow
source: alpacahack:flag-printer-2100
solved_at: 2026-05-29
---

# Flag Printer 2100

## 問題の要点

- flag を出す前に長い `sleep` が入る。
- バイナリの主処理自体は難しくなく、待ち時間を飛ばせばよい。

## 解き方

`gdb` で実行し、`sleep` 中に中断して戻り先へ jump する。

```gdb
run
# sleep 中に Ctrl-Z / interrupt
bt
jump *main_after_sleep
```

## 知見

- Rev 問題で時間待ちが本質でない場合、パッチ、LD_PRELOAD、デバッガ jump のどれかで回避できる。
- `sleep`, `nanosleep`, `clock_nanosleep` が stack trace に見えたら、呼び出し元の次命令へ飛ばす。

## 連携する知見

- [Rev](../../../insights/rev.md)
- [Rev relations](../../../relations/rev.md)
