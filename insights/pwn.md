# Pwn

Pwn は「どこに書けるか」「何を読めるか」「制御フローに届くか」を分解して考える。
CTF の小問では、保護機構を全部突破するより、用意された1つのズレを正しく exploit primitive に変換することが多い。

## 初動

- `checksec` で Canary, PIE, NX, RELRO を見る。
- 入力関数を見る: `gets`, `scanf("%s")`, `read`, `fgets` のサイズ。
- 書き込み先を見る: stack, heap, global, 配列 index, format string。
- 到達目標を見る: `win`, flag read, secret compare, function pointer, return address。

## 壊れやすい部分

- **境界チェックの片側欠落**: 上限だけ見て下限を見ないと負 index OOB。
- **隣接変数 overwrite**: 小さい overflow でも admin flag や secret を書ける。
- **format string**: `printf(user_input)` は leak/write の両方になる。追加引数があると短い payload でも強い。
- **Use-After-Free**: `free` 後に NULL 化しない pointer は、同サイズ再確保で別オブジェクトを読む/書く。
- **global buffer overflow**: ランダム secret でも secret 自体を書き換えられるなら leak 不要。
- **ret2win**: PIE 無効なら固定アドレスへ return address を上書きするだけでよい。

## 考え方

1. バグを primitive に言い換える: arbitrary write, partial overwrite, read primitive, control-flow hijack。
2. primitive の届く範囲を測る: offset、要素サイズ、符号、アラインメント。
3. 保護機構を避ける: OOB で return address へ直接書く、secret を壊す、同じ chunk を再利用する。
4. 入力制約を exploit に反映する: 文字数、NUL、改行、整数範囲、format string の出力文字数。

## 実戦メモ

- Canary があっても、return address へ直接 OOB write できるなら Canary を踏まない。
- `strcmp` は NUL で終わる。NUL overwrite は認証系で強い。
- heap 入門問では、まず「free 後に同サイズ allocate で同じアドレスになるか」を確認する。
