import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from sync_profile_readme import SyncError, main, sync


def block(name, text):
    return f"<!-- profile-sync:{name}:start -->\n\n{text}\n\n<!-- profile-sync:{name}:end -->"


SOURCE = "\n\n".join([
    "# SMF Flutter CLI",
    block("intro", "SMF generates apps.\n\n![The app](https://doc.saymyframe.com/demo/0.5/app_look.png)"),
    "## Install\n\nSee [CONTRIBUTING.md](CONTRIBUTING.md).",
    block("modules", "| Module |\n| --- |\n| [`home`](https://doc.saymyframe.com/modules/home) |"),
    block("support", "Mail support@saymyframe.com."),
])

TARGET = "\n\n".join([
    "# Say My Frame",
    block("intro", "SMF generated apps once."),
    "## Quick start\n\nRun `smf create`.",
    block("modules", "| Module |\n| --- |"),
    "## Links",
])


class SyncTest(unittest.TestCase):
    def test_copies_each_block_of_the_target_and_keeps_the_rest(self):
        self.assertEqual(
            sync(SOURCE, TARGET),
            "\n\n".join([
                "# Say My Frame",
                block("intro", "SMF generates apps.\n\n![The app](https://doc.saymyframe.com/demo/0.5/app_look.png)"),
                "## Quick start\n\nRun `smf create`.",
                block("modules", "| Module |\n| --- |\n| [`home`](https://doc.saymyframe.com/modules/home) |"),
                "## Links",
            ]),
        )

    def test_leaves_out_a_block_that_the_target_does_not_have(self):
        self.assertNotIn("support@saymyframe.com", sync(SOURCE, TARGET))

    def test_a_second_run_changes_nothing(self):
        once = sync(SOURCE, TARGET)
        self.assertEqual(sync(SOURCE, once), once)

    def test_the_blank_lines_around_a_block_do_not_matter(self):
        source = "<!-- profile-sync:intro:start -->\nText.\n\n\n<!-- profile-sync:intro:end -->"
        self.assertEqual(sync(source, block("intro", "Old.")), block("intro", "Text."))

    def test_refuses_a_target_without_blocks(self):
        with self.assertRaisesRegex(SyncError, "target has no profile-sync block"):
            sync(SOURCE, "# Say My Frame")

    def test_refuses_a_block_that_the_source_lacks(self):
        with self.assertRaisesRegex(SyncError, "source has no block news, which target has"):
            sync(SOURCE, TARGET + "\n\n" + block("news", ""))

    def test_refuses_a_relative_link_in_a_copied_block(self):
        source = block("intro", "See [the license](LICENSE), ![a logo](logo.png) and [install](#install).")
        with self.assertRaisesRegex(SyncError, "the block intro of source has relative links, .*: LICENSE, logo.png, #install"):
            sync(source, block("intro", ""))

    def test_refuses_a_relative_link_of_a_reference_or_of_html(self):
        source = block("intro", '[license]: LICENSE\n\n<img src="logo.png"> <a href="CONTRIBUTING.md">')
        with self.assertRaisesRegex(SyncError, "LICENSE, logo.png, CONTRIBUTING.md"):
            sync(source, block("intro", ""))

    def test_takes_absolute_links_and_mail(self):
        source = block("intro", '[a](https://a.example) [b](http://b.example) [c](mailto:c@example.com) <img src="https://d.example/d.png">')
        self.assertIn("mailto:c@example.com", sync(source, block("intro", "")))

    def test_a_relative_link_outside_the_copied_blocks_is_no_problem(self):
        self.assertNotIn("CONTRIBUTING.md", sync(SOURCE, TARGET))

    def test_refuses_a_start_marker_without_its_end(self):
        with self.assertRaisesRegex(SyncError, "source: the block intro has no end marker$"):
            sync("<!-- profile-sync:intro:start -->\nText.", TARGET)

    def test_refuses_a_start_marker_inside_another_block(self):
        source = "<!-- profile-sync:intro:start -->\n" + block("modules", "")
        with self.assertRaisesRegex(SyncError, "the block intro has no end marker before the start of modules"):
            sync(source, TARGET)

    def test_refuses_an_end_marker_without_its_start(self):
        with self.assertRaisesRegex(SyncError, "target: the end marker of intro has no start marker before it"):
            sync(SOURCE, TARGET + "\n<!-- profile-sync:intro:end -->")

    def test_refuses_a_block_twice(self):
        with self.assertRaisesRegex(SyncError, "target: the block intro appears twice"):
            sync(SOURCE, TARGET + "\n\n" + block("intro", ""))


class MainTest(unittest.TestCase):
    def run_main(self, source, target):
        with tempfile.TemporaryDirectory() as directory:
            source_path = Path(directory, "source.md")
            target_path = Path(directory, "README.md")
            source_path.write_text(source, encoding="utf-8")
            target_path.write_text(target, encoding="utf-8")
            output, errors = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
                code = main([str(source_path), str(target_path)])
            return code, target_path.read_text(encoding="utf-8"), output.getvalue(), errors.getvalue()

    def test_writes_the_blocks_into_the_target(self):
        code, target, output, _ = self.run_main(SOURCE, TARGET)
        self.assertEqual((code, target), (0, sync(SOURCE, TARGET)))
        self.assertIn("has the blocks of", output)

    def test_says_when_the_target_is_up_to_date(self):
        code, _, output, _ = self.run_main(SOURCE, sync(SOURCE, TARGET))
        self.assertEqual(code, 0)
        self.assertIn("is up to date", output)

    def test_leaves_the_target_as_it_is_on_an_error(self):
        code, target, _, errors = self.run_main("# No blocks", TARGET)
        self.assertEqual((code, target), (1, TARGET))
        self.assertIn("has no block intro, modules", errors)

    def test_refuses_another_number_of_arguments(self):
        errors = io.StringIO()
        with contextlib.redirect_stderr(errors):
            self.assertEqual(main(["only-one"]), 64)
        self.assertIn("Usage:", errors.getvalue())


if __name__ == "__main__":
    unittest.main()
