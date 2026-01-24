# Validation Run Design (Task 14)

## 目的
サンプルトピックで **エンドツーエンド** の実行確認を行う。

## 参照
- `.steering/20260117-validation-run/requirements.md`
- `.steering/20260117-entrypoint/design.md`

## 実行手順（例）

```
/toc-run "桃太郎" --dry-run
```

## 期待成果物

```
output/桃太郎_<timestamp>/
  research.md
  story.md
  script.md
  video.mp4   (プレースホルダでも可)
  video_manifest.md
  state.txt
```

## 検証項目

- すべてのファイルが存在する
- `state.txt` に最終ステータスが記録されている
- QAゲートの結果が `run_report.md` か manifest に記録されている

## 受け入れ条件

- 上記成果物が揃っている
- 重大なエラーで停止していない
