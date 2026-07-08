import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from content_system.editorial_style_guide import load_editorial_style_guide, validate_editorial_style_guide


class TestEditorialStyleGuide(unittest.TestCase):
    def test_style_guide_config_readable(self):
        style_guide = load_editorial_style_guide()
        self.assertIsNotNone(style_guide)
        self.assertEqual(style_guide.schema_version, "v1")

    def test_reader_profile_exists(self):
        style_guide = load_editorial_style_guide()
        self.assertTrue(len(style_guide.reader_profile.core_readers) > 0)
        self.assertTrue(len(style_guide.reader_profile.reader_needs) > 0)

    def test_principles_exist(self):
        style_guide = load_editorial_style_guide()
        self.assertTrue(len(style_guide.writing_principles) > 0)

    def test_tone_exists(self):
        style_guide = load_editorial_style_guide()
        self.assertTrue(len(style_guide.tone.preferred) > 0)
        self.assertTrue(len(style_guide.tone.discouraged) > 0)

    def test_must_have_sections(self):
        style_guide = load_editorial_style_guide()
        self.assertTrue(len(style_guide.must_have_sections) >= 5)

    def test_to_dict_serialization(self):
        style_guide = load_editorial_style_guide()
        result = style_guide.to_dict()
        self.assertIn("reader_profile", result)
        self.assertIn("writing_principles", result)
        self.assertIn("tone", result)
        self.assertIn("must_have_sections", result)

    def test_validate_returns_dict(self):
        result = validate_editorial_style_guide()
        self.assertIn("valid", result)
        self.assertIn("errors", result)
        self.assertIn("warnings", result)


if __name__ == "__main__":
    unittest.main()
