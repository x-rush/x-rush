from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SVG_NS = "http://www.w3.org/2000/svg"
NEW_ASSETS = (
    ASSETS / "banner.svg",
    ASSETS / "footer.svg",
    ASSETS / "icons" / "draftdesk.svg",
    ASSETS / "icons" / "app-dev-workflow.svg",
    ASSETS / "icons" / "photo-retouch.svg",
    ASSETS / "icons" / "image-forge.svg",
    ASSETS / "icons" / "music-forge.svg",
    ASSETS / "icons" / "video-forge.svg",
)


def local_name(tag):
    return tag.rsplit("}", 1)[-1]


class ProfileAssetTests(unittest.TestCase):
    def test_expected_pixel_assets_exist(self):
        missing = [str(path.relative_to(ROOT)) for path in NEW_ASSETS if not path.is_file()]
        self.assertEqual([], missing, "Missing profile artwork")

    def test_banner_uses_the_wide_pixel_canvas_and_palette(self):
        path = ASSETS / "banner.svg"
        root = ET.parse(path).getroot()
        source = path.read_text(encoding="utf-8")
        self.assertEqual("0 0 1280 420", root.get("viewBox"))
        for color in ("#070A12", "#0D1321", "#5DEFFF", "#9D7CFF", "#B8F35A", "#D7E1EA"):
            self.assertIn(color, source)
        self.assertIn("crispEdges", source)

    def test_banner_motion_has_a_static_reduced_motion_fallback(self):
        source = (ASSETS / "banner.svg").read_text(encoding="utf-8")
        self.assertIn("@media (prefers-reduced-motion: reduce)", source)
        self.assertRegex(source, r"animation:\s*none")

    def test_svg_assets_are_accessible(self):
        for path in ASSETS.rglob("*.svg"):
            with self.subTest(asset=str(path.relative_to(ROOT))):
                root = ET.parse(path).getroot()
                title = root.find(f"{{{SVG_NS}}}title")
                self.assertEqual("img", root.get("role"))
                self.assertTrue(root.get("aria-label") or (title is not None and title.text))

    def test_svg_assets_avoid_active_external_and_uncontrolled_content(self):
        forbidden = {"script", "filter", "animate", "animatetransform", "animatemotion", "set"}
        for path in ASSETS.rglob("*.svg"):
            with self.subTest(asset=str(path.relative_to(ROOT))):
                source = path.read_text(encoding="utf-8")
                root = ET.fromstring(source)
                for element in root.iter():
                    self.assertNotIn(local_name(element.tag).lower(), forbidden)
                    for attribute, value in element.attrib.items():
                        self.assertFalse(local_name(attribute).lower().startswith("on"))
                        if local_name(attribute) == "href":
                            self.assertTrue(value.startswith(("#", "data:")), value)
                self.assertNotIn("@import", source)
                self.assertNotRegex(source, r"url\(\s*['\"]?https?://")

    def test_local_badge_heights_match_shields(self):
        for name in ("aliyun-badge.svg", "tanstack-badge.svg", "tauri-badge.svg"):
            with self.subTest(asset=name):
                root = ET.parse(ASSETS / name).getroot()
                self.assertEqual("28", root.get("height"))
                self.assertTrue(re.fullmatch(r"[0-9.]+", root.get("width", "")))


if __name__ == "__main__":
    unittest.main()
