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

from typing import Dict, Iterable, List, Tuple

from .model import ArchitectureCandidate, PlacedModule


def _power_penalty(candidate: ArchitectureCandidate) -> Tuple[float, Dict[str, float]]:
    power_by_zone: Dict[str, float] = {}
    for pm in candidate.modules:
        power_by_zone[pm.zone.name] = power_by_zone.get(pm.zone.name, 0.0) + pm.module.max_power_kw

    penalty = 0.0
    for zone in candidate.zones:
        over = power_by_zone.get(zone.name, 0.0) - zone.max_power_kw
        if over > 0:
            penalty += over * 100.0  # harsh penalty to enforce limits
    return penalty, power_by_zone


def _harness_penalty(candidate: ArchitectureCandidate) -> float:
    if not candidate.links:
        return 0.0
    return candidate.harness_length_m * 0.5


def _estimate_latency_ms(link_latency_ms: float | None, length_m: float | None, medium: str) -> float:
    base = 0.5 if medium.lower() == "ethernet" else 2.0
    per_meter = 0.02 if medium.lower() == "ethernet" else 0.05
    estimated = link_latency_ms if link_latency_ms is not None else 0.0
    estimated = estimated or 0.0
    estimated += base
    if length_m:
        estimated += per_meter * length_m
    return estimated


def _latency_penalty(candidate: ArchitectureCandidate) -> float:
    penalty = 0.0
    for link in candidate.links:
        estimated = _estimate_latency_ms(link.latency_ms, link.length_m, link.medium)
        # Respect the strictest budget across the two zones if defined.
        budgets = [b for b in (link.src.zone.latency_budget_ms, link.dst.zone.latency_budget_ms) if b is not None]
        if budgets:
            budget = min(budgets)
            if estimated > budget:
                penalty += (estimated - budget) * 5.0
        link.latency_ms = estimated
    return penalty


def _redundancy_penalty(candidate: ArchitectureCandidate) -> float:
    penalty = 0.0
    for pm in candidate.modules:
        if pm.module.redundancy > 1:
            # Placeholder: penalize missing redundant instances.
            shortfall = pm.module.redundancy - 1
            penalty += shortfall * 25.0
    return penalty


def score_candidates(
    candidates: Iterable[ArchitectureCandidate],
) -> List[ArchitectureCandidate]:
    """
    EN:
        Compute score for each candidate architecture.

        Current scoring:
            * Base score = - total_cost
            * Penalize power limit violations
            * Penalize long harness length (rough)
            * Placeholder penalties for latency and redundancy gaps

    TR:
        Her mimari adayı için skor hesaplar.

        Güncel skor:
            * Baz skor = - toplam maliyet
            * Güç limit ihlalleri cezalandırılır
            * Kablo uzunluğu yaklaşık cezası
            * Gecikme ve yedeklilik için placeholder cezalar
    """
    scored: List[ArchitectureCandidate] = []
    for cand in candidates:
        power_penalty, power_by_zone = _power_penalty(cand)
        harness_penalty = _harness_penalty(cand)
        latency_penalty = _latency_penalty(cand)
        redundancy_penalty = _redundancy_penalty(cand)

        cand.penalties = {
            "power": power_penalty,
            "harness": harness_penalty,
            "latency": latency_penalty,
            "redundancy": redundancy_penalty,
        }
        cand.metrics = {
            "total_cost": cand.total_cost,
            "total_power_kw": cand.total_power_kw,
            "harness_length_m": cand.harness_length_m,
            "power_by_zone": power_by_zone,
        }

        total_penalty = sum(cand.penalties.values())
        cand.score = -cand.total_cost - total_penalty
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
