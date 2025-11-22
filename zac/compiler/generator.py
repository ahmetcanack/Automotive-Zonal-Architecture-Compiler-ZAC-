"""
Candidate architecture generator.

EN:
    Generates feasible zonal architecture candidates based on
    requirements and module library.

TR:
    Gereksinimler ve modül kütüphanesine göre feasible zonal
    mimari adayları üretir.
"""

from __future__ import annotations

import math
from typing import List

from .model import (
    RequirementSet,
    ModuleLibrary,
    ArchitectureCandidate,
    PlacedModule,
    Zone,
    Link,
    Module,
    Feature,
)


def _find_zone_by_name(zones: List[Zone], name: str | None) -> Zone | None:
    """
    EN:
        Helper to find a zone by name.

    TR:
        İsme göre zon bulmak için yardımcı fonksiyon.
    """
    if name is None:
        return None
    for z in zones:
        if z.name == name:
            return z
    return None


def _choose_zone(
    feature: Feature,
    module: Module,
    zones: List[Zone],
) -> Zone:
    """
    EN:
        Pick the first matching zone according to hint/candidates.

    TR:
        İpucu veya aday listesine göre ilk eşleşen zonu seçer.
    """
    if not zones:
        raise ValueError("At least one zone is required.")

    # Exact hint wins
    zone = _find_zone_by_name(zones, feature.zone_hint)
    if zone:
        return zone

    # Feature preferred zones
    for candidate in feature.zone_candidates:
        zone = _find_zone_by_name(zones, candidate)
        if zone:
            return zone

    # Module preferred zones
    for candidate in module.zone_candidates:
        zone = _find_zone_by_name(zones, candidate)
        if zone:
            return zone

    # Fallback to first zone
    return zones[0]


def _estimate_link_length(src: Zone, dst: Zone) -> float:
    """
    EN:
        Estimate cable length using zone positions if available.

    TR:
        Zon konumları varsa kablo uzunluğunu tahmin eder.
    """
    if src == dst:
        return 0.5  # small intra-zone harness

    if src.position and dst.position:
        dx = src.position[0] - dst.position[0]
        dy = src.position[1] - dst.position[1]
        return round(math.hypot(dx, dy), 2)

    # Fallback rough estimate
    return 2.5


def generate_candidates(
    requirements: RequirementSet,
    modules: ModuleLibrary,
    max_candidates: int = 10,
) -> List[ArchitectureCandidate]:
    """
    EN:
        Generate candidate zonal architectures.

        Current simple strategy:
            * For each feature, pick the first module that supports it.
            * Place that module into the hinted zone (if any), otherwise
              into the first available candidate zone.
            * Create simple point-to-point links in the order modules are added.

    TR:
        Aday zonal mimariler üretir.

        Şu anki basit strateji:
            * Her özellik için onu destekleyen ilk modülü seçer.
            * Modülü, varsa zone_hint ile belirtilen zona, yoksa ilk uygun
              aday zona yerleştirir.
            * Modüller eklenirken sıralı basit bağlantılar kurar.
    """
    if not requirements.zones:
        raise ValueError("At least one zone is required.")

    placed_modules: List[PlacedModule] = []
    links: List[Link] = []

    for feature in requirements.features:
        supporting = modules.find_supporting_modules(feature.id)
        if not supporting:
            # If a feature cannot be satisfied, skip it for now.
            # Gelecekte burada hata veya ceza puanı üretilebilir.
            continue

        mod_type = supporting[0]  # very naive choice
        zone = _choose_zone(feature, mod_type, requirements.zones)

        placed = PlacedModule(
            module=mod_type,
            zone=zone,
            provided_features=[feature.id],
        )
        placed_modules.append(placed)

        # Simple sequential link to approximate harness and latency
        if len(placed_modules) > 1:
            prev = placed_modules[-2]
            links.append(
                Link(
                    src=prev,
                    dst=placed,
                    medium="Ethernet" if mod_type.latency_class == "low" else "CAN",
                    bandwidth_mbps=100.0 if mod_type.latency_class == "low" else 10.0,
                    latency_ms=None,
                    length_m=_estimate_link_length(prev.zone, placed.zone),
                    redundant=feature.redundancy > 1,
                )
            )

    candidate = ArchitectureCandidate(
        zones=requirements.zones,
        modules=placed_modules,
        links=links,
    )

    # Only one candidate for now; later we can extend to multiple.
    return [candidate][:max_candidates]
