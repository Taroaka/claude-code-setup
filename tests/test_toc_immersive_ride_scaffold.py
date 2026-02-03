import subprocess
import sys
import unittest
from pathlib import Path


class TestTocImmersiveRideScaffold(unittest.TestCase):
    def test_scaffold_creates_expected_files(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory(prefix="toc_test_out_") as td:
            base = Path(td) / "out"
            base.mkdir(parents=True, exist_ok=True)

            subprocess.run(
                [
                    sys.executable,
                    "scripts/toc-immersive-ride.py",
                    "--topic",
                    "テスト トピック",
                    "--timestamp",
                    "20990101_0000",
                    "--base",
                    str(base),
                    "--force",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            run_dir = base / "テスト_トピック_20990101_0000"
            self.assertTrue((run_dir / "state.txt").exists())
            self.assertTrue((run_dir / "research.md").exists())
            self.assertTrue((run_dir / "story.md").exists())
            self.assertTrue((run_dir / "script.md").exists())
            self.assertTrue((run_dir / "video_manifest.md").exists())
            self.assertTrue((run_dir / "assets" / "characters").is_dir())
            self.assertTrue((run_dir / "assets" / "scenes").is_dir())
            self.assertTrue((run_dir / "assets" / "audio").is_dir())


if __name__ == "__main__":
    unittest.main()

