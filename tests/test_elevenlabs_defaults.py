import os
import unittest

from toc.providers.elevenlabs import DEFAULT_ELEVENLABS_VOICE_ID, ElevenLabsConfig


class TestElevenLabsDefaults(unittest.TestCase):
    def test_from_env_falls_back_to_default_voice_id(self) -> None:
        old = os.environ.get("ELEVENLABS_VOICE_ID")
        try:
            if "ELEVENLABS_VOICE_ID" in os.environ:
                del os.environ["ELEVENLABS_VOICE_ID"]
            cfg = ElevenLabsConfig.from_env(api_key="test_key")
            self.assertEqual(cfg.voice_id, DEFAULT_ELEVENLABS_VOICE_ID)
        finally:
            if old is None:
                os.environ.pop("ELEVENLABS_VOICE_ID", None)
            else:
                os.environ["ELEVENLABS_VOICE_ID"] = old


if __name__ == "__main__":
    unittest.main()

