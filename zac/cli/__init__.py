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


def _add_compile_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "requirements",
        type=Path,
        help=(
            "EN: Path to requirements/features JSON file. "
            "TR: Gereksinim/özellik JSON dosyasının yolu."
        ),
    )
    parser.add_argument(
        "modules",
        type=Path,
        help=(
            "EN: Path to module library JSON file. "
            "TR: Modül kütüphanesi JSON dosyasının yolu."
        ),
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("out.json"),
        help=(
            "EN: Output JSON path for selected architecture (default: out.json). "
            "TR: Seçilen mimarinin yazılacağı çıktı JSON yolu (varsayılan: out.json)."
        ),
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="zac",
        description=(
            "ZAC – Zonal Architecture Compiler\n"
            "EN: Compile vehicle-level requirements into zonal architectures.\n"
            "TR: Araç gereksinimlerinden zonal mimariler üret."
        ),
    )

    subparsers = parser.add_subparsers(dest="command")
    compile_parser = subparsers.add_parser(
        "compile",
        help="EN: Compile requirements and modules. TR: Gereksinim ve modülleri derle.",
    )
    _add_compile_args(compile_parser)

    # Legacy flags (kept for contract compatibility)
    parser.add_argument(
        "--requirements",
        type=Path,
        help=(
            "EN: Path to requirements JSON file. "
            "TR: Gereksinim JSON dosyasının yolu."
        ),
    )
    parser.add_argument(
        "--modules",
        type=Path,
        help=(
            "EN: Path to module library JSON file. "
            "TR: Modül kütüphanesi JSON dosyasının yolu."
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        help=(
            "EN: Output JSON path for selected architecture. "
            "TR: Seçilen mimarinin yazılacağı çıktı JSON yolu."
        ),
    )
    return parser


def _resolve_paths(args: argparse.Namespace, parser: argparse.ArgumentParser) -> tuple[Path, Path, Path]:
    if args.command == "compile":
        return args.requirements, args.modules, args.output

    if args.requirements and args.modules:
        output = args.output or Path("out.json")
        return args.requirements, args.modules, output

    parser.error("Provide 'zac compile <requirements> <modules> [--output]' or legacy --requirements/--modules flags.")


def main() -> None:
    """
    EN:
        Entry point for the ZAC CLI.

    TR:
        ZAC komut satırı aracının giriş noktası.
    """
    parser = _build_parser()
    args = parser.parse_args()

    requirements_path, modules_path, output_path = _resolve_paths(args, parser)

    # === Load inputs ===
    req_set = loader.load_requirements(requirements_path)
    module_lib = loader.load_module_library(modules_path)

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
    loader.dump_architecture(best, output_path)

    print(f"✔ Architecture saved to: {output_path}")


if __name__ == "__main__":
    # EN: Allow `python -m zac.cli` for debugging if you want.
    # TR: İstersen `python -m zac.cli` ile debug amaçlı çalıştırmaya izin verir.
    main()
