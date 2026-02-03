# Immersive Ride POV Slash Command: Tasklist

## 1) Spec / docs

- [ ] `.claude/commands/toc/toc-immersive-ride.md` を追加
- [ ] `docs/implementation/immersive-ride-entrypoint.md` を追加（正本）
- [ ] `docs/how-to-run.md` / `docs/README.md` にリンク追加
- [ ] `AGENTS.md` と `CLAUDE.md` に新コマンドを追記（同一内容維持）

## 2) Agents

- [ ] `immersive-scriptwriter` を追加（story → script + manifest）

## 3) Implementation helpers

- [ ] `scripts/toc-immersive-ride.py`（run dir 作成 + state + placeholders）

## 4) Pipeline extensions (minimal)

- [ ] Gemini image: 参照画像（multi-image）を `parts:inlineData` として送れるよう拡張
- [ ] Veo video: `first_frame` / `last_frame` を manifest で扱えるように拡張（可能な範囲で）
- [ ] `scripts/render-video.sh` に `--fps` / `--size` を追加（1280x720/24fps）

## 5) Validation

- [ ] `python -m compileall .` が通る
- [ ] `scripts/toc-immersive-ride.py --topic "X" --dry-run` で run dir が生成される

