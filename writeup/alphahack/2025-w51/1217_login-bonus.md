---
title: login-bonus
category: pwn
genre: global-overwrite
difficulty: medium
tags:
  - scanf-overflow
  - global-buffer
  - strcmp
source: alpacahack:login-bonus
solved_at: 2026-05-29
---

# login-bonus

## 問題の要点

- `password` と `secret` が隣接する 32 byte のグローバル変数。
- `secret` は起動ごとにランダムだが、`password` 入力の `scanf` に長さ制限がない。
- `strcmp(password, secret)` が通ればよい。

## 解き方

overflow で `secret` 側を `password` と同じ値にする。ヌルバイトで両方を空文字扱いにできるなら、32個程度の `\0` で比較が通る。

```bash
(printf '\0%.0s' {1..32}; cat) | ./login
```

## 知見

- secret がランダムでも、secret 自体を書き換えられるなら leak は不要。
- `strcmp` は最初の NUL で終わるため、NUL 注入・NUL overwrite は認証バイパスになりやすい。

## 連携する知見

- [Pwn](../../../insights/pwn.md)
- [Pwn relations](../../../relations/pwn.md)
