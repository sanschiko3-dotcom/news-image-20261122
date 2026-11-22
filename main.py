"""Entrypoint: verify assets/entry.png and copy it to the output dir.

Standard library only. The PNG is checked by its signature bytes, its
size (<= 1,048,576 bytes) and its IHDR chunk (width/height each <= 1024),
then copied byte-for-byte to $MAKEFUN_OUTPUT_DIR (default /output) as
entry.png. The written file is re-read and compared byte-for-byte.
"""
import hashlib
import os
import shutil
import struct
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576
MAX_DIMENSION = 1024


def sha256_hex(data):
    return hashlib.sha256(data).hexdigest()


def read_ihdr_dimensions(data):
    """Return (width, height) from the PNG IHDR chunk."""
    if len(data) < 33:
        raise ValueError("file too short to be a PNG")
    if data[:8] != PNG_SIGNATURE:
        raise ValueError("not a PNG file (bad signature)")
    length = struct.unpack(">I", data[8:12])[0]
    chunk_type = data[12:16]
    if chunk_type != b"IHDR" or length != 13:
        raise ValueError("first chunk is not a 13-byte IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "assets", "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    dst = os.path.join(out_dir, "entry.png")
    with open(src, "rb") as fh:
        data = fh.read()
    if len(data) > MAX_BYTES:
        raise ValueError(f"entry.png is {len(data)} bytes, over the "
                         f"{MAX_BYTES}-byte limit")
    width, height = read_ihdr_dimensions(data)
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        raise ValueError(f"entry.png is {width}x{height}, over the "
                         f"{MAX_DIMENSION}x{MAX_DIMENSION} limit")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)
    with open(dst, "rb") as fh:
        written = fh.read()
    if written != data:
        raise ValueError("written entry.png differs from the source")
    print(f"{dst} {width}x{height} {len(written)} bytes "
          f"sha256={sha256_hex(written)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
