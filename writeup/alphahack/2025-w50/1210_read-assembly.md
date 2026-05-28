---
title: Read Assembly
category: rev
genre: assembly
difficulty: medium
tags:
  - aarch64
  - control-flow
  - fibonacci
source: alpacahack:read-assembly
solved_at: 2026-05-29
---

# Read Assembly

## 問題の要点

- AArch64 の短い assembly を読み、最終的に出力される値を flag に入れる。
- レジスタ更新と分岐だけで構成されるため、C に写経すると意味が見える。

## 解き方

レジスタを変数に写してループを再現する。

```c
int w0 = 0, w1 = 0, w4 = 1, w2 = 0, w3 = 0;
while (1) {
    w3 = w2 + w4;
    if ((w1 & 1) == 0) {
        w0 += w3;
        w1++;
    }
    w1++;
    if (w1 == 0x28) break;
    w4 = w2;
    w2 = w3;
}
printf("%d\n", w0);
```

フィボナッチ数列に関係する値の和になり、答えは `102334155`。

## 得られた flag

```text
Alpaca{102334155}
```

## 知見

- assembly rev は「命令名を全部覚える」より、レジスタ更新を高級言語に戻すのが速い。
- ループ変数、状態変数、条件分岐を分けると数列や checksum が見えやすい。

## 連携する知見

- [Rev](../../../insights/rev.md)
- [Rev relations](../../../relations/rev.md)
