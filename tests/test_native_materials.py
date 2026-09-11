"""Regression checks for native file termination and material completeness."""
import unittest
from scripts.native_asset_checks import parse_sample_material


def component(name):
    return "\n".join((
        "$SUBMATERIAL " + name,
        "$TEXTURE_MTL 0 diffuse.dds",
        "$TEXTURE_MTL 1 specular.dds",
        "$TEXTURE_MTL 2 normal.dds",
        "$DIFFUSECOLOR 1 1 1 1",
        "$SPECULARCOLOR 0 0 0 1",
        "$AMBIENTCOLOR 1 1 1 1",
        "",
    ))


class NativeMaterialTests(unittest.TestCase):
    def test_all_components_precede_one_file_terminator(self):
        parsed = parse_sample_material(component("hall") + component("yard") + "$END\n")
        self.assertEqual([part["name"] for part in parsed], ["hall", "yard"])

    def test_reject_original_premature_termination(self):
        broken = component("hall") + "$END\n" + component("yard") + "$END\n"
        with self.assertRaisesRegex(ValueError, r"after \$END"):
            parse_sample_material(broken)

    def test_reject_missing_terminator(self):
        with self.assertRaisesRegex(ValueError, "Missing final"):
            parse_sample_material(component("hall"))

    def test_reject_duplicate_names(self):
        with self.assertRaisesRegex(ValueError, "duplicate submaterial"):
            parse_sample_material(component("hall") + component("hall") + "$END\n")

    def test_reject_incomplete_textures(self):
        broken = component("hall").replace("$TEXTURE_MTL 2 normal.dds\n", "") + "$END\n"
        with self.assertRaisesRegex(ValueError, "Incomplete texture"):
            parse_sample_material(broken)

    def test_reject_duplicate_texture_slot(self):
        broken = component("hall") + "$TEXTURE_MTL 0 other.dds\n$END\n"
        with self.assertRaisesRegex(ValueError, "Duplicate texture"):
            parse_sample_material(broken)


if __name__ == "__main__":
    unittest.main()
