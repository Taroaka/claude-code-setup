# /toc-run

ToC（TikTok Story Creator）をトピックから実行するためのコマンド。

## 使い方（想定）

```
/toc-run "桃太郎" --dry-run
```

## 期待される出力

- `output/<topic>_<timestamp>/` が作成される
- `state.txt`（追記型）が生成される

詳細は `docs/how-to-run.md` を参照。
