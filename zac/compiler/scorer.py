"""
Scoring utilities for architecture candidates.

EN:
    Interfaces (in the future) with the Rust optimizer and provides helper
    functions to select the best architecture.

TR:
    Gelecekte Rust optimize edici ile konuşacak ve en iyi mimariyi
    seçmek için yardımcı fonksiyonlar sağlayacak modül.
"""

from __future__ import annotations

from typing import Iterable, List

from .model import ArchitectureCandidate


def score_candidates(
    candidates: Iterable[ArchitectureCandidate],
) -> List[ArchitectureCandidate]:
    """
    EN:
        Compute score for each candidate architecture.

        Current simple scoring:
            * score = - total_cost
            (cheaper architectures get higher scores)

    TR:
        Her mimari adayı için skor hesaplar.

        Şu anki basit skor:
            * score = - total_cost
            (daha ucuz mimari daha yüksek puan alır)
    """
    scored: List[ArchitectureCandidate] = []
    for cand in candidates:
        cand.score = -cand.total_cost
        scored.append(cand)
    return scored


def select_best(candidates: Iterable[ArchitectureCandidate]) -> ArchitectureCandidate:
    """
    EN:
        Select the best candidate based on score.

    TR:
        Skora göre en iyi adayı seçer.
    """
    candidates = list(candidates)
    if not candidates:
        raise ValueError("No candidates to select from.")

    # If score is None, treat as 0.0
    return max(candidates, key=lambda c: (c.score or 0.0))