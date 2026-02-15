import json
import subprocess
import sys
import unittest
from pathlib import Path


class TestManifestTimestampParsing(unittest.TestCase):
    def test_make_vertical_short_dry_run_parses_and_trims(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory(prefix="toc_ts_test_") as td:
            run_dir = Path(td) / "out" / "topic_20990101_0000"
            run_dir.mkdir(parents=True, exist_ok=True)

            # Approved state gate.
            (run_dir / "state.txt").write_text(
                "\n".join(
                    [
                        "review.video.status=approved",
                        "artifact.video=video.mp4",
                        "---",
                        "",
                    ]
                ),
                encoding="utf-8",
            )

            # Dummy video file (dry-run does not invoke ffmpeg).
            (run_dir / "video.mp4").write_bytes(b"")

            manifest = run_dir / "video_manifest.md"
            manifest.write_text(
                "\n".join(
                    [
                        "# Manifest",
                        "",
                        "```yaml",
                        "video_metadata:",
                        '  topic: "テストトピック"',
                        "scenes:",
                        "  - scene_id: 10",
                        '    timestamp: "00:00-00:08"',
                        "  - scene_id: 20",
                        '    timestamp: "00:08-00:16"',
                        "```",
                        "",
                    ]
                ),
                encoding="utf-8",
            )

            out_path = run_dir / "shorts" / "short01.mp4"
            r = subprocess.run(
                [
                    sys.executable,
                    "scripts/make-vertical-short.py",
                    "--run-dir",
                    str(run_dir),
                    "--scene-ids",
                    "10,20",
                    "--duration-seconds",
                    "10",
                    "--out",
                    str(out_path),
                    "--dry-run",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            payload = json.loads(r.stdout)
            self.assertEqual(Path(payload["video"]).name, "video.mp4")
            self.assertEqual(Path(payload["out"]).name, "short01.mp4")

            segs = payload["segments"]
            self.assertEqual(len(segs), 2)
            self.assertEqual(segs[0]["scene_id"], 10)
            self.assertEqual(segs[0]["start"], 0)
            self.assertEqual(segs[0]["end"], 8)
            self.assertEqual(segs[1]["scene_id"], 20)
            self.assertEqual(segs[1]["start"], 8)
            self.assertEqual(segs[1]["end"], 10)  # trimmed to fit 10s total


if __name__ == "__main__":
    unittest.main()

