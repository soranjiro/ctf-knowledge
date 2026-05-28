---
title: power_obfus_royalty
category: rev
genre: powershell
difficulty: medium
tags:
  - powershell
  - obfuscation
  - deobfuscation
source: alpacahack:power-obfus-royalty
solved_at: 2026-05-29
---

# power_obfus_royalty

## 問題の要点

- PowerShell の難読化コードを読む問題。
- Invoke-Expression、文字列結合、エンコード/デコードの層を剥がす。

## 解き方

1. 実行される文字列を直接実行せず、出力するように置き換える。
2. Base64、文字列 reverse、置換などの変換を CyberChef や手元スクリプトで剥がす。
3. 最終的に出てくる flag 文字列を読む。

## 得られた flag

```text
TSGLIVE{1nv0k3_3xpr35510n_15_an_1mp0r7an7_f3a7ur3_f0r_p0w3r5h3ll_0bfu5ca710n}
```

## 知見

- 難読化 rev は、まず「実行される文字列」を表示に変える。
- PowerShell の `Invoke-Expression` は eval 相当なので、そこに渡る直前の値が主戦場。

## 連携する知見

- [Rev](../../../insights/rev.md)
- [Rev relations](../../../relations/rev.md)
