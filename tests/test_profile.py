from html.parser import HTMLParser
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
    ASSETS / "banner-mobile.svg",
    ASSETS / "footer-mobile.svg",
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

    def test_mobile_artwork_has_readable_canvas_and_type(self):
        cases = (("banner-mobile.svg", "0 0 640 640", 18), ("footer-mobile.svg", "0 0 640 240", 20))
        for name, view_box, minimum_font_size in cases:
            with self.subTest(asset=name):
                path = ASSETS / name
                self.assertTrue(path.is_file(), f"Missing mobile artwork: {name}")
                root = ET.parse(path).getroot()
                self.assertEqual(view_box, root.get("viewBox"))
                text_elements = list(root.iter(f"{{{SVG_NS}}}text"))
                self.assertTrue(text_elements)
                for text in text_elements:
                    self.assertGreaterEqual(float(text.get("font-size", "0")), minimum_font_size)

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


class ProfileMarkupParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
        self.sources = []
        self.source_sets = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "img":
            self.images.append(attributes)
        if tag == "source":
            self.sources.append(attributes)
        if tag == "source" and attributes.get("srcset"):
            self.source_sets.append(attributes["srcset"])


class ProfileReadmeTests(unittest.TestCase):
    def setUp(self):
        self.source = (ROOT / "README.md").read_text(encoding="utf-8")
        self.parser = ProfileMarkupParser()
        self.parser.feed(self.source)

    def inventory_images(self):
        if "## 05 / INVENTORY" not in self.source or "## 06 / SYSTEM METRICS" not in self.source:
            return []
        inventory = self.source.split("## 05 / INVENTORY", 1)[1].split("## 06 / SYSTEM METRICS", 1)[0]
        parser = ProfileMarkupParser()
        parser.feed(inventory)
        return parser.images

    def test_profile_has_the_seven_console_sections(self):
        for heading in (
            "## 01 / WHOAMI",
            "## 02 / PARTY MEMBERS",
            "## 03 / ACTIVE QUESTS",
            "## 04 / FORGE SYSTEM",
            "## 05 / INVENTORY",
            "## 06 / SYSTEM METRICS",
            "## 07 / CURRENTLY",
        ):
            self.assertTrue(heading in self.source, f"Missing section: {heading}")

    def test_original_projects_and_current_ventures_survive(self):
        for project in (
            "draftdesk",
            "app-dev-workflow",
            "photo-retouch",
            "image-forge",
            "music-forge",
            "video-forge",
        ):
            self.assertIn(f"https://github.com/x-rush/{project}", self.source)
        for venture in (
            "multi-platform content matrix",
            "AI SaaS sites --going-global",
            "creative apps portfolio",
            "cross-border e-commerce",
        ):
            self.assertIn(venture, self.source)

    def test_local_art_replaces_template_widgets(self):
        sources = [image.get("src", "") for image in self.parser.images]
        self.assertTrue("assets/banner.svg" in sources, "Missing local banner")
        self.assertTrue("assets/footer.svg" in sources, "Missing local footer")
        self.assertNotIn("readme-typing-svg", self.source)
        self.assertNotIn("capsule-render", self.source)

    def test_narrow_screens_get_dedicated_artwork(self):
        mobile_sources = [
            source.get("srcset")
            for source in self.parser.sources
            if source.get("media") == "(max-width: 640px)"
        ]
        self.assertCountEqual(["assets/banner-mobile.svg", "assets/footer-mobile.svg"], mobile_sources)

    def test_images_have_alt_text_and_local_files_exist(self):
        for image in self.parser.images:
            with self.subTest(image=image.get("src")):
                self.assertTrue(image.get("alt", "").strip())
                src = image.get("src", "")
                if src and not src.startswith(("https://", "http://", "data:")):
                    self.assertTrue((ROOT / src.split("?", 1)[0]).is_file(), src)
        for srcset in self.parser.source_sets:
            for candidate in srcset.split(","):
                src = candidate.strip().split()[0]
                if not src.startswith(("https://", "http://", "data:")):
                    self.assertTrue((ROOT / src.split("?", 1)[0]).is_file(), src)

    def test_readme_has_no_fixed_width_page_container(self):
        self.assertNotIn("min-width", self.source)
        self.assertNotRegex(self.source, r"(?<![a-zA-Z-])width\s*:")
        self.assertNotIn("<table width", self.source)
        self.assertNotIn("<details", self.source.lower())

    def test_inventory_preserves_every_original_badge_exactly_once(self):
        expected = [
            "TypeScript", "JavaScript", "Python", "Go", "PHP", "Java", "Rust",
            "React", "Next.js", "Vue.js", "Vite", "TanStack", "React Native", "Tauri", "PWA",
            "Express", "FastAPI", "Spring Boot", "Laravel", "Gin",
            "MySQL", "PostgreSQL", "MongoDB", "Redis", "SQLite",
            "Docker", "Kubernetes", "Nginx", "Linux", "Node.js", "Git", "GitHub Actions", "CloudBase", "Aliyun",
            "fal.ai", "Replicate", "ffmpeg", "Prompt Engineering", "Agent Skills",
        ]
        actual = [image.get("alt") for image in self.inventory_images()]
        self.assertEqual(39, len(expected))
        self.assertCountEqual(expected, actual)

    def test_inventory_badges_keep_consistent_source_styles(self):
        for image in self.inventory_images():
            src = image.get("src", "")
            with self.subTest(badge=image.get("alt")):
                if "img.shields.io" in src:
                    self.assertIn("style=for-the-badge", src)
                if src.endswith("-badge.svg"):
                    root = ET.parse(ROOT / src).getroot()
                    self.assertEqual("28", root.get("height"))

    def test_stats_keep_light_and_dark_picture_variants(self):
        self.assertGreaterEqual(self.source.count("<picture>"), 2)
        self.assertGreaterEqual(self.source.count('media="(prefers-color-scheme: dark)"'), 2)
        self.assertTrue("github-profile-summary-cards.vercel.app/api/cards/stats" in self.source, "Missing stats card")
        self.assertTrue("github-profile-summary-cards.vercel.app/api/cards/most-commit-language" in self.source, "Missing language card")
        self.assertTrue("theme=tokyonight" in self.source, "Missing accessible dark stats theme")
        self.assertTrue("theme=default" in self.source, "Missing light stats theme")
        self.assertNotIn("github-readme-stats.vercel.app", self.source)


if __name__ == "__main__":
    unittest.main()
