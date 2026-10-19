"""Copies the profile-sync blocks of a README into another README.

A block starts at a line `<!-- profile-sync:<name>:start -->` and ends at the
line `<!-- profile-sync:<name>:end -->`. Each block of the target takes the text
of the block of the same name in the source, and the rest of the target stays as
it is. A block of the source that the target does not have is left out.

Usage: sync_profile_readme.py <source> <target>

The script rewrites the target only when its blocks change. It exits with 1 and
leaves the target as it is when a file has a marker without its pair or a block
twice, when the target has no block or a block that the source lacks, and when a
copied block has a relative link, which would be broken on the page of the
organization.
"""

import os
import re
import sys
from pathlib import Path

MARKER = re.compile(r"^<!-- profile-sync:([a-z0-9-]+):(start|end) -->$", re.MULTILINE)

# The targets of inline links and images, of reference definitions, and of the
# href and src of HTML.
LINK_TARGETS = (
    re.compile(r"\]\(\s*<?([^)\s>]+)"),
    re.compile(r"^ {0,3}\[[^\]]+\]:\s*<?([^\s>]+)", re.MULTILINE),
    re.compile(r"\b(?:href|src)\s*=\s*[\"']([^\"']+)", re.IGNORECASE),
)

ABSOLUTE = re.compile(r"^(?:https?:|mailto:)", re.IGNORECASE)


class SyncError(Exception):
    pass


def blocks(text, file):
    """Returns the span of the text of each block, by its name."""
    found = {}
    name = None
    for marker in MARKER.finditer(text):
        marker_name, kind = marker.groups()
        if kind == "start":
            if name is not None:
                raise SyncError(f"{file}: the block {name} has no end marker before the start of {marker_name}")
            if marker_name in found:
                raise SyncError(f"{file}: the block {marker_name} appears twice")
            name, start = marker_name, marker.end()
        else:
            if marker_name != name:
                raise SyncError(f"{file}: the end marker of {marker_name} has no start marker before it")
            found[name] = (start, marker.start())
            name = None
    if name is not None:
        raise SyncError(f"{file}: the block {name} has no end marker")
    return found


def relative_links(text):
    return [
        link
        for pattern in LINK_TARGETS
        for link in pattern.findall(text)
        if not ABSOLUTE.match(link)
    ]


def sync(source, target, source_file="source", target_file="target"):
    """Returns the target with the text of each of its blocks from the source."""
    source_blocks = blocks(source, source_file)
    target_blocks = blocks(target, target_file)
    if not target_blocks:
        raise SyncError(f"{target_file} has no profile-sync block")
    missing = [name for name in target_blocks if name not in source_blocks]
    if missing:
        raise SyncError(f"{source_file} has no block {', '.join(missing)}, which {target_file} has")

    texts = {}
    for name in target_blocks:
        start, end = source_blocks[name]
        text = source[start:end].strip("\n")
        links = relative_links(text)
        if links:
            raise SyncError(
                f"the block {name} of {source_file} has relative links, which the page of the "
                f"organization cannot resolve: {', '.join(links)}"
            )
        texts[name] = text

    result = target
    for name, (start, end) in sorted(target_blocks.items(), key=lambda block: block[1], reverse=True):
        result = f"{result[:start]}\n\n{texts[name]}\n\n{result[end:]}"
    return result


def main(arguments):
    if len(arguments) != 2:
        print("Usage: sync_profile_readme.py <source> <target>", file=sys.stderr)
        return 64
    source_file, target_file = arguments
    target_path = Path(target_file)
    target = target_path.read_text(encoding="utf-8")
    try:
        result = sync(Path(source_file).read_text(encoding="utf-8"), target, source_file, target_file)
    except SyncError as error:
        prefix = "::error::" if os.environ.get("GITHUB_ACTIONS") == "true" else "error: "
        print(f"{prefix}{error}", file=sys.stderr)
        return 1
    if result == target:
        print(f"{target_file} is up to date.")
    else:
        target_path.write_text(result, encoding="utf-8")
        print(f"{target_file} has the blocks of {source_file} now.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
