# Tasklist: cinematic object/setpiece bible（manifest-first）

## 1) Data contract（manifest）

- [ ] `workflow/immersive-ride-video-manifest-template.md` に `assets.object_bible` と `object_ids` を追加
- [ ] `workflow/immersive-cloud-island-walk-video-manifest-template.md` に同様の追加

## 2) Generator（注入 + ゲート）

- [ ] `scripts/generate-assets-from-manifest.py` に `assets.object_bible` を追加パース
- [ ] `scripts/generate-assets-from-manifest.py` に `object_ids` を scene パース
- [ ] `scripts/generate-assets-from-manifest.py` で `[PROPS / SETPIECES]` へ注入
- [ ] `--require-object-ids` / `--require-object-reference-scenes` を追加

## 3) Scaffold / wrapper

- [ ] `scripts/toc-immersive-ride.py` で `assets/objects/` を作る
- [ ] `scripts/toc-immersive-ride-generate.sh` で新ゲートを常時 ON

## 4) Docs / playbooks / skills

- [ ] `docs/implementation/asset-bibles.md` を追加（浦島太郎例含む）
- [ ] `docs/implementation/image-prompting.md` を更新（`PROPS / SETPIECES`）
- [ ] `docs/data-contracts.md` に immersive manifest の契約追記
- [ ] `workflow/playbooks/script/hero-journey-cinematic-setpieces.md` を追加（スキル編）
- [ ] `.codex/skills/hero-journey-cinematic-setpieces/SKILL.md` を追加

## 5) Tests

- [ ] object_bible 注入の unit test 追加
- [ ] validation（object_ids / reference scene）テスト追加
- [ ] `python -m compileall .` / `python -m unittest discover -s tests`

