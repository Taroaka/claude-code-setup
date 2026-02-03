import subprocess
import sys
import unittest


class TestGenerateVeoVideoCli(unittest.TestCase):
    def test_dry_run_includes_last_image_field(self) -> None:
        proc = subprocess.run(
            [
                sys.executable,
                "scripts/generate-veo-video.py",
                "--dry-run",
                "--prompt",
                "p",
                "--out",
                "out.mp4",
                "--input-image",
                "first.png",
                "--last-image",
                "last.png",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("endImage", proc.stdout)


if __name__ == "__main__":
    unittest.main()

