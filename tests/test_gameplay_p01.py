"""Independent coordinate and installation-safety checks for the local prototype."""
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from types import SimpleNamespace
from unittest.mock import patch
from scripts.gameplay_p01 import native,building_text,SOURCE,workshop_text,legacy_manifest_matches
from scripts.prepare_gameplay_p01 import require_game_closed


class GameplayP01Tests(unittest.TestCase):
    def test_historical_manifest_survives_git_line_endings(self):
        original=b'{\r\n  "revision": "a04"\r\n}\r\n'
        expected=hashlib.sha256(original).hexdigest()
        with TemporaryDirectory() as directory:
            path=Path(directory)/'verification.json'
            for content in (original,original.replace(b'\r\n',b'\n')):
                path.write_bytes(content)
                self.assertTrue(legacy_manifest_matches(path,expected))

    def test_historical_manifest_rejects_content_change(self):
        expected=hashlib.sha256(b'{"revision":"a04"}\r\n').hexdigest()
        with TemporaryDirectory() as directory:
            path=Path(directory)/'verification.json'
            path.write_bytes(b'{"revision":"a05"}\n')
            self.assertFalse(legacy_manifest_matches(path,expected))

    def test_known_coordinate_landmarks(self):
        self.assertEqual(native([75,56,0]),(0,0,0))
        self.assertEqual(native([24,1,11]),(-51,11,55))
        self.assertEqual(native([72,119,0]),(-3,0,-63))
        self.assertEqual(native([149,82,5.2]),(74,5.2,-26))

    def test_native_misspelling_and_no_combustion_inputs(self):
        d=json.loads((SOURCE/'definition.json').read_text(encoding='utf-8'))
        text=building_text(d)
        process=[line for line in text.splitlines() if line.startswith('$CONSUMPTION')]
        self.assertEqual(process,['$CONSUMPTION_PER_SECOND eletric 0.5'])
        self.assertNotIn('$PARTICLE',text)

    def test_owner_is_numeric_and_local_item_private(self):
        d=json.loads((SOURCE/'definition.json').read_text(encoding='utf-8'))
        with self.assertRaises(ValueError):
            workshop_text(d,'1\n$VISIBILITY 0')
        self.assertIn('$VISIBILITY 2',workshop_text(d,0))

    def test_running_game_prevents_installation(self):
        result=SimpleNamespace(stdout='"SOVIET64.exe","123","Console","1","100 K"\n')
        with patch('scripts.prepare_gameplay_p01.os.name','nt'),patch(
                'scripts.prepare_gameplay_p01.subprocess.run',return_value=result):
            with self.assertRaisesRegex(ValueError,'close W&R'):
                require_game_closed()

    def test_running_viewer_prevents_installation(self):
        result=SimpleNamespace(stdout='"ModelViewer.exe","123","Console","1","100 K"\n')
        with patch('scripts.prepare_gameplay_p01.os.name','nt'),patch(
                'scripts.prepare_gameplay_p01.subprocess.run',return_value=result):
            with self.assertRaisesRegex(ValueError,'ModelViewer'):
                require_game_closed()


if __name__=='__main__':
    unittest.main()
