"""
ZAC CLI package.

EN:
    Provides the main command-line interface for ZAC.
    This is what runs when you call:
        python -m zac
    or the console script:
        zac

TR:
    ZAC için ana komut satırı arayüzünü sağlar.
    Şu komutlar çalıştığında burası devreye girer:
        python -m zac
    veya console script:
        zac
"""

from __future__ import annotations

import argparse
from pathlib import Path

from zac.compiler import loader, generator, scorer


def main() -> None:
    """
    EN:
        Entry point for the ZAC CLI.

    TR:
        ZAC komut satırı aracının giriş noktası.
    """
    parser = argparse.ArgumentParser(
        prog="zac",
        description=(
            "ZAC – Zonal Architecture Compiler\n"
            "EN: Compile vehicle-level requirements into zonal architectures.\n"
            "TR: Araç gereksinimlerinden zonal mimariler üret."
        ),
    )

    parser.add_argument(
        "--requirements",
        type=Path,
        required=True,
        help=(
            "EN: Path to requirements JSON file. "
            "TR: Gereksinim JSON dosyasının yolu."
        ),
    )

    parser.add_argument(
        "--modules",
        type=Path,
        required=True,
        help=(
            "EN: Path to module library JSON file. "
            "TR: Modül kütüphanesi JSON dosyasının yolu."
        ),
    )

    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help=(
            "EN: Output JSON path for selected architecture. "
            "TR: Seçilen mimarinin yazılacağı çıktı JSON yolu."
        ),
    )

    args = parser.parse_args()

    # === Load inputs ===
    req_set = loader.load_requirements(args.requirements)
    module_lib = loader.load_module_library(args.modules)

    # === Generate candidates ===
    candidates = generator.generate_candidates(
        requirements=req_set,
        modules=module_lib,
        max_candidates=10,
    )

    # === Score ===
    scored = scorer.score_candidates(candidates)
    best = scorer.select_best(scored)

    # === Dump output ===
    loader.dump_architecture(best, args.output)

    print(f"✔ Architecture saved to: {args.output}")


if __name__ == "__main__":
    # EN: Allow `python -m zac.cli` for debugging if you want.
    # TR: İstersen `python -m zac.cli` ile debug amaçlı çalıştırmaya izin verir.
    main()