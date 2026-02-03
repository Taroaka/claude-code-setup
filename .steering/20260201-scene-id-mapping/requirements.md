# Requirements: 調査→story/script の scene_id 配賦

## 背景

story/script を scene に分割して生成する前提で、調査で集めた情報を「どの scene で使うか」整理できていないと、
裏話/小ネタが前に出たり、逆に情報が捨てられて story/script が薄くなりやすい。

## 期待する改善

- 調査の段階で scene を最低20分割し、`scene_id` を保持する
- 収集した情報（hooks / tensions / open_questions など）に `scene_ids` を付与して配賦する
- 全体に効く情報は opening/ending に寄せ、途中のネタは該当シーンへ割り当てる

## 制約

- コードで強制しない（運用・テンプレ・エージェント指示で担保する）

