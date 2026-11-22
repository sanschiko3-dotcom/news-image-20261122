"""Publish the prepared front-page image as the competition entry.

The grader runs this module with no network and no third-party packages,
so it uses only the standard library. The picture itself is rendered ahead
of time by render.py and shipped in this repository as assets/entry.png;
this module verifies that file, then writes an identical copy to the
output directory named by MAKEFUN_OUTPUT_DIR (default /output).

Running the module twice writes byte-identical files, because it copies
fixed bytes and never depends on the clock, randomness, or the network.
"""

import hashlib
import os
import sys
from pathlib import Path

ENTRY_NAME = "entry.png"
MAX_ENTRY_BYTES = 1_048_576
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def source_path():
    """Absolute path of the bundled image sitting beside this file."""
    return Path(__file__).resolve().parent / "assets" / ENTRY_NAME


def output_dir():
    """Output directory from the environment, defaulting to /output."""
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def checked_bytes(path):
    """Read the bundled image and reject anything that is not a small PNG."""
    if not path.is_file():
        raise FileNotFoundError(
            "Prepared entry image is missing: {0}".format(path)
        )
    data = path.read_bytes()
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError(
            "Prepared entry image is not a PNG file: {0}".format(path)
        )
    if len(data) > MAX_ENTRY_BYTES:
        raise ValueError(
            "Prepared entry image exceeds 1 MiB: {0} bytes".format(len(data))
        )
    if len(data) < 33 or data[12:16] != b"IHDR":
        raise ValueError(
            "Prepared entry image has no PNG header chunk: {0}".format(path)
        )
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    if width > 1024 or height > 1024:
        raise ValueError(
            "Prepared entry image is {0}x{1}, over the 1024x1024 cap".format(
                width, height
            )
        )
    return data


def publish():
    """Write the verified image to the output directory and report it.

    The write is re-read and compared byte for byte before the digest is
    printed, so a truncated or partial write can never pass silently.
    """
    data = checked_bytes(source_path())
    target_dir = output_dir()
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / ENTRY_NAME
    target.write_bytes(data)
    written = target.read_bytes()
    if written != data:
        raise ValueError("Written entry does not match the source image")
    digest = hashlib.sha256(data).hexdigest()
    print("{0} {1} bytes sha256={2}".format(target, len(data), digest))
    return 0


def main():
    return publish()


if __name__ == "__main__":
    sys.exit(main())
