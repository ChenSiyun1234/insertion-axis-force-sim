"""Build the host DLL and compile the controller for Cortex-M4F."""

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def build(arm_only=False):
    output_directory = ROOT / "build"
    output_directory.mkdir(exist_ok=True)
    environment = os.environ.copy()
    compiler = [sys.executable, "-m", "ziglang", "cc"]
    common_flags = [
        "-std=c99",
        "-Wall",
        "-Wextra",
        "-Werror",
        "-O2",
        "-Ifirmware/include",
    ]
    sources = sorted(
        str(source.relative_to(ROOT)) for source in (ROOT / "firmware/src").glob("*.c")
    )
    if not arm_only:
        subprocess.run(
            compiler
            + common_flags
            + ["-DAXIS_SIL", "-shared"]
            + sources
            + ["-o", "build/axis_fw.dll"],
            cwd=ROOT,
            env=environment,
            check=True,
        )
    for source in sources:
        arm_object = output_directory / (Path(source).stem + ".o")
        subprocess.run(
            compiler
            + ["-target", "thumb-freestanding-eabihf", "-mcpu=cortex_m4"]
            + common_flags
            + ["-c", source, "-o", str(arm_object)],
            cwd=ROOT,
            env=environment,
            check=True,
        )
    prefix = "" if arm_only else "Host DLL built; "
    print(f"{prefix}ARM compile check passed ({len(sources)} sources).")


if __name__ == "__main__":
    build("--arm-only" in sys.argv)
