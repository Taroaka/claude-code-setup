# ToC Agent Guide

このファイルは複数モデルのAIエージェントに対してのドキュメントとするため、 **`AGENTS.md` と `CLAUDE.md` で同一内容**として管理する（差分を作らない）。

## リポジトリの個性（北極星）

1) **AIエージェントが開発を進める**前提で、進め方（要求→設計→タスク）をドキュメント化している  
2) **物語トピック→動画生成**を Claude Code の **slash command** から簡単に実行できる（想定）

## 起動（Claude Code slash command）

- 起点: `/toc-run`
- 使い方（想定）: `/toc-run "topic" [--dry-run] [--config <path>]`
- コマンド説明: `.claude/commands/toc/toc-run.md`
- 実行手順（全体）: `docs/how-to-run.md`

## state 管理（ファイル）

state は **コード内の状態ではなく**、プロジェクトフォルダの **テキスト**で管理する。

- 置き場所: `output/<topic>_<timestamp>/state.txt`
- 形式: key=value（簡易テキスト）
- 更新方式: **追記型**
  - ブロック区切りは `---`
  - 最新ブロックが現在状態
- 再開: 最新ブロックを読み込んで続きから進める
- 擬似ロールバック: 過去ブロックをコピーし、必要なキーを変更して末尾に追記
- スキーマ: `workflow/state-schema.txt`

## ドキュメント構成（どこに何があるか）

- 恒久仕様: `docs/`（入口は `docs/README.md`）
- 実装に直結する正本: `docs/implementation/`（`.steering` から昇華した仕様）
- 作業単位の履歴: `.steering/`（`requirements.md` → `design.md` → `tasklist.md`）
- テンプレ/契約: `workflow/`（`workflow/*-template.yaml`, `workflow/state-schema.txt`）
- 実行支援: `scripts/`
- 設定: `config/`（例: `config/system.yaml`）
- Claude Code: `.claude/commands/`（/toc-run など）
- 生成物: `output/`（原則 gitignore 対象）

## 進め方（spec-first）

- 変更が非自明なら `.steering/YYYYMMDD-<title>/` を作り、
  `requirements.md` → `design.md` → `tasklist.md` の順で固める（必要なら各段階で承認を取る）
- 実装は **設計に沿って最小変更**で行う（依頼されたこと以外はしない）
- 変更後は可能な範囲で検証（例: `python -m compileall .`、CI想定のdry-runなど）

## Secrets / env

- `.env.example` を `.env` にコピーして利用
- シークレットは絶対にコミットしない

---

## ALWAYS START WITH THESE COMMANDS FOR COMMON TASKS

**Task: "List/summarize all files and directories"**

```bash
fd . -t f           # Lists ALL files recursively (FASTEST)
# OR
rg --files          # Lists files (respects .gitignore)
```

**Task: "Search for content in files"**

```bash
rg "search_term"    # Search everywhere (FASTEST)
```

**Task: "Find files by name"**

```bash
fd "filename"       # Find by name pattern (FASTEST)
```

### Directory/File Exploration

```bash
# FIRST CHOICE - List all files/dirs recursively:
fd . -t f           # All files (fastest)
fd . -t d           # All directories
rg --files          # All files (respects .gitignore)

# For current directory only:
ls -la              # OK for single directory view
```

### BANNED - Never Use These Slow Tools

* ❌ `tree` - NOT INSTALLED, use `fd` instead
* ❌ `find` - use `fd` or `rg --files`
* ❌ `grep` or `grep -r` - use `rg` instead
* ❌ `ls -R` - use `rg --files` or `fd`
* ❌ `cat file | grep` - use `rg pattern file`

### Use These Faster Tools Instead

```bash
# ripgrep (rg) - content search
rg "search_term"                # Search in all files
rg -i "case_insensitive"        # Case-insensitive
rg "pattern" -t py              # Only Python files
rg "pattern" -g "*.md"          # Only Markdown
rg -n "pattern"                 # Show line numbers
rg -A 3 -B 3 "error"            # Context lines

# ripgrep (rg) - file listing
rg --files                      # List files (respects .gitignore)
rg --files | rg "pattern"       # Find files by name

# fd - file finding
fd -e md                        # All .md files

# jq - JSON processing
jq . data.json                  # Pretty-print
```

### Search Strategy

1. Start broad, then narrow: `rg "partial" | rg "specific"`
2. Filter by type early: `rg -t python "def function_name"`
3. Batch patterns: `rg "(pattern1|pattern2|pattern3)"`
4. Limit scope: `rg "pattern" src/`

### INSTANT DECISION TREE

```
User asks to "list/show/summarize/explore files"?
  → USE: fd . -t f  (fastest, shows all files)
  → OR: rg --files  (respects .gitignore)

User asks to "search/grep/find text content"?
  → USE: rg "pattern"  (NOT grep!)

User asks to "find file/directory by name"?
  → USE: fd "name"  (NOT find!)

User asks for "directory structure/tree"?
  → USE: fd . -t d  (directories) + fd . -t f  (files)
  → NEVER: tree (not installed!)

Need just current directory?
  → USE: ls -la  (OK for single dir)
```
