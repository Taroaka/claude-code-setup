# Validation Run Requirements (Task 14)

## 目的
既知トピックでサンプル実行し、成果物が正しく生成されることを確認する。

## 参照
- `.steering/20260117-entrypoint/design.md`
- `.steering/20260117-video-integration/design.md`
- `docs/orchestration-and-ops.md`

## スコープ
- 1つのサンプルトピックによる実行
- 生成成果物の存在確認
- QAゲートの通過確認

## 前提
- プレースホルダ生成でもOK
- 出力は `output/<topic>_<timestamp>/`

## 要件

- サンプルトピック: 「桃太郎」
- `research.md`, `story.md`, `script.md`, `video.mp4` が生成される
- `video_manifest.md` と `state.txt` が生成される
- QAゲートが pass する（少なくとも実行可能）

## 受け入れ条件
- 成果物の存在が確認できる
- QAゲートの結果が記録されている
