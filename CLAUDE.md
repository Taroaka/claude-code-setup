# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## AI Guidance

* Ignore GEMINI.md and GEMINI-*.md files
* To save main context space, for code searches, inspections, troubleshooting or analysis, use code-searcher subagent where appropriate - giving the subagent full context background for the task(s) you assign it.
* After receiving tool results, carefully reflect on their quality and determine optimal next steps before proceeding. Use your thinking to plan and iterate based on this new information, and then take the best next action.
* For maximum efficiency, whenever you need to perform multiple independent operations, invoke all relevant tools simultaneously rather than sequentially.
* Before you finish, please verify your solution
* Do what has been asked; nothing more, nothing less.
* NEVER create files unless they're absolutely necessary for achieving your goal.
* ALWAYS prefer editing an existing file to creating a new one.
* NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested by the User.
* When you update or modify core context files, also update markdown documentation and memory bank
* When asked to commit changes, exclude CLAUDE.md and CLAUDE-*.md referenced memory bank system files from any commits. Never delete these files.

## Memory Bank System

This project uses a structured memory bank system with specialized context files. Always check these files for relevant information before starting work:

### Core Context Files

* **CLAUDE-activeContext.md** - Current session state, goals, and progress (if exists)
* **CLAUDE-patterns.md** - Established code patterns and conventions (if exists)
* **CLAUDE-decisions.md** - Architecture decisions and rationale (if exists)
* **CLAUDE-troubleshooting.md** - Common issues and proven solutions (if exists)
* **CLAUDE-config-variables.md** - Configuration variables reference (if exists)
* **CLAUDE-temp.md** - Temporary scratch pad (only read when referenced)

**Important:** Always reference the active context file first to understand what's currently being worked on and maintain session continuity.

### Memory Bank System Backups

When asked to backup Memory Bank System files, you will copy the core context files above and @.claude settings directory to directory @/path/to/backup-directory. If files already exist in the backup directory, you will overwrite them.

## Claude Code Official Documentation

When working on Claude Code features (hooks, skills, subagents, MCP servers, etc.), use the `claude-docs-consultant` skill to selectively fetch official documentation from docs.claude.com.

## Project Overview

### TikTok Story Creator (ToC)

**概要:**
AIエージェントが自律的に情報収集し、物語を生成してTikTok向けの縦型動画（1分程度）を自動作成するシステム。

**目的:**
- TikTok動画による収益化
- 完全自動化されたコンテンツ生成パイプライン
- スケーラブルな動画制作システム

### システムフロー

1. **手動実行トリガー** - ユーザーがシステムを起動
2. **情報収集フェーズ** - AIエージェントが`docs/information-gathering.md`を参照して情報収集
3. **物語生成フェーズ** - `docs/story-creation.md`を参照して収集情報を物語に加工
4. **動画生成フェーズ** - 物語から縦型動画(9:16)を生成
5. **出力** - 1分程度のMP4ファイル

### 技術スタック

**言語・フレームワーク:**
- Python 3.11+
- FastAPI (必要に応じて管理API)

**AI・生成モデル（最新版使用）:**
- **LLM:** OpenAI GPT-5.2 / Claude 4.0 Sonnet (切替可能)
- **音声合成:** ElevenLabs / OpenAI TTS / Google TTS (切替可能)
- **画像生成:** DALL-E 3 / Stable Diffusion 3.5 (切替可能)
- **動画生成AI（複数プロバイダー対応）:**
  - Google Veo 3.1
  - OpenAI Sora 2
  - Kling AI
  - Runway Gen-3
  - Pika Labs
  - Stability AI (Stable Video Diffusion)

**動画処理:**
- FFmpeg - 動画編集・エンコード
- MoviePy - Python動画生成ライブラリ
- Pillow/PIL - 画像処理

**データベース:**
- PostgreSQL - 動画メタデータ、物語、生成履歴、設定

**インフラ:**
- Docker/Docker Compose - コンテナ化
- 手動実行

### アーキテクチャ

```
[手動実行トリガー]
    ↓
[AIエージェント] ← docs/information-gathering.md
    ↓ 情報収集
[物語生成エンジン] ← docs/story-creation.md
    ↓ テキスト処理
[マルチメディア生成]
    ├─ 音声合成
    ├─ 画像生成
    └─ 動画生成AI (選択可能)
    ↓
[動画レンダリング (FFmpeg/MoviePy)]
    ↓
[出力: 縦型MP4 (9:16, ~1分)]
```

### 主要コンポーネント

1. **情報収集エージェント**
   - `docs/information-gathering.md`に記載された手順に従う
   - トレンド、ニュース、テーマの収集

2. **物語生成エンジン**
   - `docs/story-creation.md`に記載された加工方法に従う
   - LLM (GPT-5.2/Claude 4.0) によるストーリー作成

3. **マルチメディア生成**
   - 音声合成 (ElevenLabs/OpenAI TTS/Google TTS)
   - 画像生成 (DALL-E 3/SD 3.5)
   - 動画生成AI (Veo 3.1/Sora 2/Kling/Runway/Pika)

4. **動画レンダリング**
   - FFmpeg/MoviePyによる動画合成
   - 字幕、エフェクト、BGM統合

5. **メタデータ管理**
   - PostgreSQLでの履歴・統計・設定管理

### 設定管理

- プロバイダー切替: `config/providers.yaml`
- AI APIキー: `.env`ファイル
- 動画生成設定: `config/video_settings.yaml`



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
rg -1 "pattern"                 # Filenames with matches
rg -c "pattern"                 # Count matches per file
rg -n "pattern"                 # Show line numbers 
rg -A 3 -B 3 "error"            # Context lines
rg " (TODO| FIXME | HACK)"      # Multiple patterns

# ripgrep (rg) - file listing 
rg --files                      # List files (respects •gitignore)
rg --files | rg "pattern"       # Find files by name 
rg --files -t md                # Only Markdown files 

# fd - file finding 
fd -e js                        # All •js files (fast find) 
fd -x command {}                # Exec per-file 
fd -e md -x ls -la {}           # Example with ls 

# jq - JSON processing 
jq. data.json                   # Pretty-print 
jq -r .name file.json           # Extract field 
jq '.id = 0' x.json             # Modify field
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
