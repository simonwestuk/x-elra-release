"""Build sanitized HTML fragments from Markdown content files.

This script walks the ``content`` directory, renders Markdown files to HTML,
records any custom hint blocks, and writes the sanitized output to
``static/content`` while preserving the directory structure.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from html import escape
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import bleach
import markdown
import yaml

BASE_DIR = Path(__file__).resolve().parents[1]
CONTENT_DIR = BASE_DIR / "content"
OUTPUT_DIR = BASE_DIR / "static" / "content"

HINT_BLOCK_RE = re.compile(
    r":::hint(?:[ \t]+(?P<title>[^\n]+))?\n(?P<body>.*?)(?:\n)?:::(?:\n|$)",
    re.DOTALL,
)

ANSWER_BLOCK_RE = re.compile(
    r":::answer(?:[ \t]+(?P<title>[^\n]+))?\n(?P<body>.*?)(?:\n)?:::(?:\n|$)",
    re.DOTALL,
)

EXPECTED_OUTPUT_BLOCK_RE = re.compile(
    r":::expected_output\n(?P<body>.*?)(?:\n)?:::(?:\n|$)",
    re.DOTALL,
)

ALLOWED_TAGS = sorted({
    *bleach.sanitizer.ALLOWED_TAGS,
    "p",
    "pre",
    "code",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "table",
    "thead",
    "tbody",
    "tr",
    "td",
    "th",
    "blockquote",
    "img",
    "figure",
    "figcaption",
    "span",
    "div",
    "details",
    "summary",
})

ALLOWED_ATTRIBUTES = {
    **bleach.sanitizer.ALLOWED_ATTRIBUTES,
    "a": {"href", "title", "rel", "target"},
    "img": {"src", "alt", "title", "loading"},
    "code": {"class", "data-expected-output"},
    "pre": {"class", "data-expected-output"},
    "div": {"class", "data-hint", "data-title", "data-expected-output", "hidden"},
    "span": {"class"},
    "details": {"class"},
    "summary": {"class"},
}

ALLOWED_PROTOCOLS = bleach.sanitizer.ALLOWED_PROTOCOLS | {"data"}

LIVE_CODE_FENCE_RE = re.compile(
    r"^```(?P<lang>[a-zA-Z0-9_+-]+)(?P<meta>[^\n]*)$",
    re.MULTILINE,
)


def rewrite_live_code_blocks(markdown_body: str) -> str:
    """Normalise `` ```python live`` fences to Markdown attribute syntax."""

    def _replace(match: re.Match[str]) -> str:
        lang = (match.group("lang") or "").strip()
        meta = (match.group("meta") or "").strip()
        if not lang or lang.lower() != "python":
            return match.group(0)
        if not meta:
            return match.group(0)
        tokens = [token for token in meta.split() if token]
        if not tokens:
            return match.group(0)
        has_live = any(token.lower() == "live" for token in tokens)
        if not has_live:
            return match.group(0)
        remaining = [token for token in tokens if token.lower() != "live"]
        classes = [f".{lang.lower()}", ".live"]
        attributes: List[str] = []
        for token in remaining:
            if token.startswith("."):
                classes.append(token)
            elif "=" in token:
                attributes.append(token)
            else:
                classes.append(f".{token}")
        attr_parts = classes + attributes
        attr_block = " ".join(attr_parts)
        return f"```{{{attr_block}}}"

    return LIVE_CODE_FENCE_RE.sub(_replace, markdown_body)


@dataclass
class RenderedContent:
    """Representation of a rendered Markdown document."""

    front_matter: Dict[str, object]
    html: str
    hints: List[Dict[str, str]]
    answers: List[Dict[str, str]]
    slug: str
    source_path: Path
    output_path: Path


def parse_front_matter(text: str) -> Tuple[Dict[str, object], str]:
    """Split a Markdown document into YAML front matter and body."""

    if not text.startswith("---\n"):
        return {}, text

    lines = text.splitlines()
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            front_matter_text = "\n".join(lines[1:idx])
            body = "\n".join(lines[idx + 1 :])
            data = yaml.safe_load(front_matter_text) or {}
            if not isinstance(data, dict):
                raise ValueError("Front matter must be a mapping of keys to values")
            return data, body
    # Unterminated front matter block
    raise ValueError("Front matter block starting with '---' is not closed")


def slugify(value: str) -> str:
    """Normalise a slug value to be filesystem and URL friendly."""

    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value or "index"


def extract_hints(markdown_body: str) -> Tuple[List[Dict[str, str]], str]:
    """Extract custom hint blocks and convert them to Markdown-friendly text."""

    hints: List[Dict[str, str]] = []

    def _replacement(match: re.Match[str]) -> str:
        title = (match.group("title") or "").strip()
        body = match.group("body").strip()
        hints.append({"title": title, "content": body})
        heading = f"Hint: {title}" if title else "Hint"
        # Represent hints as blockquotes for Markdown rendering.
        quoted_lines = [f"> **{heading}**"]
        for line in body.splitlines():
            quoted_lines.append("> " + line)
        return "\n".join(quoted_lines)

    transformed = HINT_BLOCK_RE.sub(_replacement, markdown_body)
    return hints, transformed


def extract_answers(markdown_body: str) -> Tuple[List[Dict[str, str]], str]:
    """Extract custom answer blocks and convert them to ``<details>`` elements."""

    answers: List[Dict[str, str]] = []

    def _replacement(match: re.Match[str]) -> str:
        title = (match.group("title") or "").strip()
        body = match.group("body").strip()
        answers.append({"title": title, "content": body})
        summary_text = title if title else "Reveal answer"
        # Render body through Markdown so code fences etc. work inside answers.
        body_html = markdown.markdown(
            body,
            extensions=["fenced_code", "tables", "attr_list"],
            output_format="html5",
        )
        return (
            f'<details class="xelra-answer">'
            f"<summary>{escape(summary_text)}</summary>\n"
            f"{body_html}"
            f"</details>"
        )

    transformed = ANSWER_BLOCK_RE.sub(_replacement, markdown_body)
    return answers, transformed


def extract_expected_outputs(markdown_body: str) -> str:
    """Attach ``:::expected_output`` blocks to the preceding ``python live`` fence.

    Each ``:::expected_output`` block is removed from the body and its content
    is injected as a ``data-expected-output`` key-value pair in the attribute
    block of the immediately preceding live code fence.  This allows the
    front-end widget to compare actual stdout against the expected value.
    """

    def _inject_attr(body: str, output_text: str) -> str:
        """Find the last ``python live`` fence before the current position
        and add the expected-output data attribute to its attribute block."""
        escaped = escape(output_text).replace("\n", "&#10;")
        # The rewrite_live_code_blocks step hasn't run yet at this point so
        # fences still look like ```python live …
        # We add a data attribute that rewrite_live_code_blocks will carry
        # through.  But actually, it's simpler to inject a raw HTML comment
        # that the JS can read.  However the cleanest approach is: convert
        # the :::expected_output block into a hidden <div> right after the
        # code fence, which the JS can pick up as a sibling.
        return (
            f'\n<div class="xelra-expected-output" hidden '
            f'data-expected-output="{escaped}"></div>\n'
        )

    parts = EXPECTED_OUTPUT_BLOCK_RE.split(markdown_body)
    # re.split with one group produces [before, body1, after1, body2, after2, ...]
    if len(parts) == 1:
        return markdown_body
    result_parts: List[str] = []
    for i, part in enumerate(parts):
        if i % 2 == 0:
            # Text between (or before/after) expected_output blocks
            result_parts.append(part)
        else:
            # This is the captured body of an :::expected_output block
            result_parts.append(_inject_attr(markdown_body, part.strip()))
    return "".join(result_parts)


def render_markdown(markdown_text: str) -> str:
    """Render Markdown to HTML using a consistent extension set."""

    return markdown.markdown(
        markdown_text,
        extensions=["fenced_code", "tables", "attr_list"],
        output_format="html5",
    )


def sanitize_html(html_fragment: str) -> str:
    """Strip unsafe HTML while preserving useful formatting."""

    return bleach.clean(
        html_fragment,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        strip=True,
    )


def render_document(path: Path, content_root: Path = CONTENT_DIR, output_root: Path = OUTPUT_DIR) -> RenderedContent:
    """Render a single Markdown file to sanitized HTML."""

    text = path.read_text(encoding="utf-8")
    front_matter, body = parse_front_matter(text)
    hints, markdown_body = extract_hints(body)
    answers, markdown_body = extract_answers(markdown_body)
    markdown_body = extract_expected_outputs(markdown_body)
    markdown_body = rewrite_live_code_blocks(markdown_body)

    slug_source = str(front_matter.get("slug") or path.stem)
    slug = slugify(slug_source)

    html_fragment = render_markdown(markdown_body)
    clean_html = sanitize_html(html_fragment)

    relative_parent = path.relative_to(content_root).parent
    output_dir = output_root / relative_parent
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{slug}.html"

    metadata_comment = json.dumps(front_matter, ensure_ascii=False)
    output_html = "\n".join(
        [
            "<!-- Generated by scripts/build_content.py; do not edit by hand -->",
            f"<!-- front-matter: {escape(metadata_comment)} -->",
            clean_html,
        ]
    )
    output_path.write_text(output_html, encoding="utf-8")

    return RenderedContent(
        front_matter=front_matter,
        html=clean_html,
        hints=hints,
        answers=answers,
        slug=slug,
        source_path=path,
        output_path=output_path,
    )


def iter_markdown_files(content_root: Path = CONTENT_DIR) -> Iterable[Path]:
    """Yield all Markdown files under the content root."""

    if not content_root.exists():
        return []
    return sorted(p for p in content_root.rglob("*.md") if p.is_file())


def build_all(content_root: Path = CONTENT_DIR, output_root: Path = OUTPUT_DIR) -> List[RenderedContent]:
    """Render every Markdown file under ``content_root``."""

    rendered: List[RenderedContent] = []
    for md_path in iter_markdown_files(content_root):
        rendered.append(render_document(md_path, content_root, output_root))
    return rendered


def main() -> None:
    parser = argparse.ArgumentParser(description="Render Markdown content into static HTML")
    parser.add_argument(
        "--content-dir",
        default=str(CONTENT_DIR),
        help="Directory containing Markdown files (default: %(default)s)",
    )
    parser.add_argument(
        "--output-dir",
        default=str(OUTPUT_DIR),
        help="Directory to write rendered HTML (default: %(default)s)",
    )
    args = parser.parse_args()

    content_root = Path(args.content_dir).resolve()
    output_root = Path(args.output_dir).resolve()

    if not content_root.exists():
        print(f"No content directory found at {content_root}, skipping")
        output_root.mkdir(parents=True, exist_ok=True)
        return

    rendered = build_all(content_root, output_root)
    if not rendered:
        print("No Markdown files found in content directory")
    else:
        for item in rendered:
            print(f"Rendered {item.source_path.relative_to(content_root)} -> {item.output_path.relative_to(output_root)}")


if __name__ == "__main__":
    main()
