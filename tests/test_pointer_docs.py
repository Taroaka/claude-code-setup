import subprocess
import sys
import unittest
from pathlib import Path


class TestPointerDocs(unittest.TestCase):
    def test_root_pointer_docs_validate(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/validate-pointer-docs.py", "--root", str(Path(".").resolve())],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("Pointer docs valid.", result.stdout)


if __name__ == "__main__":
    unittest.main()
