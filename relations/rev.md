# Rev Relations

Rev 関連 writeup の index。
「比較点を読む」「変換を逆にする」「solver に落とす」のどれかで探す。

## 関連 insights

- [Rev](../insights/rev.md)

## 事例一覧

- [Leaked Flag Checker](../writeup/alphahack/2025-w49/1204_leaked-flag-checker.md): 小さい checker を angr で探索する。
- [Read Assembly](../writeup/alphahack/2025-w50/1210_read-assembly.md): AArch64 を C に写して数列計算を読む。
- [Sugoi Flag Checker](../writeup/alphahack/2025-w50/1212_sugoi-flag-checker.md): `strcmp` 直前の平文 expected を debugger で読む。
- [power_obfus_royalty](../writeup/alphahack/2025-w50/1214_power-obfus-royalty.md): PowerShell の eval 直前の文字列を剥がす。
- [Flag Printer 2100](../writeup/alphahack/2025-w51/1215_flag-printer-2100.md): 長い sleep を debugger jump で飛ばす。
- [Twilight](../writeup/alphahack/2025-w51/1218_twilight.md): 関数ポインタで index ごとに変換が変わる出力列を逆変換する。
- [Useful Machine](../writeup/alphahack/2025-w52/1226_useful-machine.md): 独自 VM を Z3 BitVec で symbolic execution する。
- [cha-ll-enge](../writeup/alphahack/2025-w52/1228_cha-ll-enge.md): LLVM IR の key 配列から XOR 条件を解く。

## 比較観点

- 平文比較: `Sugoi Flag Checker`
- 可逆変換: `Twilight`, `cha-ll-enge`
- solver/探索: `Leaked Flag Checker`, `Useful Machine`
- assembly/IR 読解: `Read Assembly`, `cha-ll-enge`
- 難読化/待ち回避: `power_obfus_royalty`, `Flag Printer 2100`
