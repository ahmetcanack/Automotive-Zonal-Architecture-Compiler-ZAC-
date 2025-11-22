"""
Scoring utilities for architecture candidates.

EN:
  Interfaces with the Rust optimizer (future) and provides helper
  functions to select the best architecture.

TR:
  Rust optimize edici (gelecekte) ile konuşan ve en iyi mimariyi
  seçmek için yardımcı fonksiyonlar sağlayan modül.
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

    TR:
      Her mimari adayı için skor hesaplar.

    Notes / Notlar
    --------------
    EN:
      For now, this is a dummy implementation assigning score=0.0.
      Later this will call into the Rust optimization library.

    TR:
      Şimdilik her adaya score=0.0 atayan sahte bir implementasyon.
      İleride Rust optimize edici kütüphaneye çağrı yapacak.
    """
    scored: List[ArchitectureCandidate] = []
    for cand in candidates:
        cand.score = 0.0
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

    return max(candidates, key=lambda c: (c.score or 0.0))