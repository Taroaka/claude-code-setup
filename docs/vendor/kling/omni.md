# Kling 3.0 Omni メモ（差分吸収のための要点）

現時点での Omni は「通常 Kling 3.0 とは入力/出力が増える」可能性が高いので、このrepoでは以下の方針で吸収します。

## このrepoでの扱い

- manifest: `video_generation.tool: "kling_3_0_omni"`
- モデル切替: `KLING_OMNI_VIDEO_MODEL`（または CLI の `--kling-omni-video-model`）
- Omni 固有パラメータ: `KLING_OMNI_EXTRA_JSON`（または `--kling-omni-extra-json`）

## 参考: 代表的な Omni 機能（第三者ドキュメント起点）

第三者ドキュメントでは、Omni に以下のような概念が出てきます（名称・フィールドはゲートウェイにより変動し得ます）。

- 音声生成の on/off
- マルチショット（複数カットを 1 回で生成）
- 参照画像の番号参照（プロンプト内で `@image_1` のように参照する流儀）

参照: PiAPI の Kling 3.0 Omni API（リンクは `README.md`）。

## 推奨運用

1. まず `--dry-run` / provider log の JSON を見て、通したい Omni パラメータを決める
2. `KLING_OMNI_EXTRA_JSON` で透過する
3. よく使うものだけを manifest/schema に昇格する

