"""
Command-line interface for ZAC.

EN:
    Provides the `zac` command used to compile architectures.

TR:
    Mimarileri derlemek için kullanılan `zac` komut satırı arayüzünü sağlar.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from .compiler import loader, generator, scorer


def main() -> None:
    """
    EN:
        Entry point for the `zac` CLI.

    TR:
        `zac` komut satırı aracının giriş noktası.
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

    req_set = loader.load_requirements(args.requirements)
    module_lib = loader.load_module_library(args.modules)

    candidates = generator.generate_candidates(
        requirements=req_set,
        modules=module_lib,
        max_candidates=10,
    )

    scored = scorer.score_candidates(candidates)
    best = scorer.select_best(scored)

    loader.dump_architecture(best, args.output)