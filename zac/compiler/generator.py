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

from typing import List

from .model import (
    RequirementSet,
    ModuleLibrary,
    ArchitectureCandidate,
    PlacedModule,
    Zone,
    Link,
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


def generate_candidates(
    requirements: RequirementSet,
    modules: ModuleLibrary,
    max_candidates: int = 10,
) -> List[ArchitectureCandidate]:
    """
    EN:
        Generate candidate zonal architectures.

        Current simple strategy:
            * For each requirement, pick the first module that supports it.
            * Place that module into the hinted zone (if any), otherwise
              into the first zone.
            * Ignore wiring and safety details for now.

    TR:
        Aday zonal mimariler üretir.

        Şu anki basit strateji:
            * Her gereksinim için onu destekleyen ilk modülü seçer.
            * Modülü, varsa zone_hint ile belirtilen zona, yoksa ilk zona
              yerleştirir.
            * Şimdilik kablolama ve güvenlik detaylarını yok sayar.
    """
    if not requirements.zones:
        raise ValueError("At least one zone is required.")

    placed_modules: List[PlacedModule] = []

    for req in requirements.requirements:
        supporting = modules.find_supporting_modules(req.id)
        if not supporting:
            # If a requirement cannot be satisfied, skip it for now.
            # Gelecekte burada hata veya ceza puanı üretilebilir.
            continue

        mod_type = supporting[0]  # very naive choice

        zone = _find_zone_by_name(requirements.zones, req.zone_hint)
        if zone is None:
            zone = requirements.zones[0]

        placed_modules.append(PlacedModule(module_type=mod_type, zone=zone))

    # For now we do not generate any explicit links.
    links: List[Link] = []

    candidate = ArchitectureCandidate(
        zones=requirements.zones,
        modules=placed_modules,
        links=links,
    )

    # Only one candidate for now; later we can extend to multiple.
    return [candidate][:max_candidates]