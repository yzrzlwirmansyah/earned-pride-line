"""earned-pride-line: write one line of earned pride to entry.txt.

Stdlib only, deterministic, no network, no randomness.
Writes the line plus a trailing newline to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output), then re-reads the
file and verifies it matches exactly.
"""

import os
import sys

LINE = (
    "After two years of physio, Dani took one unaided step across "
    "his kitchen, then another, while his wife held her breath at "
    "the door."
)


def main() -> int:
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = os.path.join(output_dir, "entry.txt")

    # Fail fast on an out-of-range line: never write an invalid entry.
    if not 1 <= len(LINE) <= 240:
        print(
            "self-verification failed: line length %d out of range 1-240" % len(LINE),
            file=sys.stderr,
        )
        return 1

    os.makedirs(output_dir, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(LINE + "\n")

    # Post-write self-verification: re-read raw bytes and assert exact
    # contents, valid UTF-8, exactly one line, no trailing spaces,
    # and a single trailing newline.
    with open(path, "rb") as f:
        raw = f.read()
    try:
        written = raw.decode("utf-8")
    except UnicodeDecodeError:
        print("self-verification failed: file is not valid UTF-8", file=sys.stderr)
        return 1
    if written != LINE + "\n":
        print("self-verification failed: file contents do not match", file=sys.stderr)
        return 1
    if written.count("\n") != 1:
        print("self-verification failed: file does not contain exactly one line", file=sys.stderr)
        return 1
    if written.endswith(" \n") or written.endswith("\n\n"):
        print("self-verification failed: trailing spaces or double newline", file=sys.stderr)
        return 1
    if LINE != LINE.strip() or "  " in LINE:
        print("self-verification failed: line has leading/trailing/double spaces", file=sys.stderr)
        return 1
    print("wrote %s (%d chars)" % (path, len(LINE)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
