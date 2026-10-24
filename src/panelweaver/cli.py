"""The panelweaver command line."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from panelweaver import __version__


def _qa_render(args: argparse.Namespace) -> int:
    from panelweaver.qa.render import PROFILES, check_render

    profile = PROFILES[args.profile]
    if args.size:
        w, h = (int(v) for v in args.size.lower().split("x"))
        profile = profile.model_copy(update={"width": w, "height": h})
    report = check_render(Path(args.video), profile)
    if args.json:
        print(report.model_dump_json(indent=2))
    else:
        for c in report.checks:
            print(f"{'PASS' if c.passed else 'FAIL'}  {c.name}: {c.detail}")
        print("PASSED" if report.passed else "FAILED")
    return 0 if report.passed else 1


def _validate(args: argparse.Namespace) -> int:
    from pydantic import ValidationError

    from panelweaver.schemas.annotation import ChapterAnnotation, ReferenceTimeline

    failed = 0
    for path in args.files:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        model = ReferenceTimeline if "video_id" in data else ChapterAnnotation
        try:
            model.model_validate(data)
            print(f"ok    {path}")
        except ValidationError as e:
            failed += 1
            print(f"FAIL  {path}\n{e}")
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="panelweaver")
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(required=True)

    qa = sub.add_parser("qa-render", help="check a rendered MP4 (docs/SUCCESS_CRITERIA.md)")
    qa.add_argument("video")
    qa.add_argument("--profile", choices=["final", "preview"], default="final")
    qa.add_argument("--size", help="override the expected size, e.g. 320x180")
    qa.add_argument("--json", action="store_true")
    qa.set_defaults(func=_qa_render)

    val = sub.add_parser("validate", help="validate eval annotation files")
    val.add_argument("files", nargs="+")
    val.set_defaults(func=_validate)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
