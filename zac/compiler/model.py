"""
Core data models for ZAC.

EN:
  Defines the internal representation of requirements, zones,
  modules, links and architecture candidates.

TR:
  Gereksinimler, zonlar, modüller, bağlantılar ve mimari adayları için
  ZAC'in dahili veri temsilini tanımlar.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Requirement:
    """
    EN:
      High-level vehicle requirement (e.g. 'front camera', 'ABS', 'ADAS ECU').

    TR:
      Yüksek seviyeli araç gereksinimi (örn. 'ön kamera', 'ABS', 'ADAS ECU').
    """
    id: str
    name: str
    zone_hint: Optional[str] = None
    safety_level: Optional[str] = None


@dataclass
class Zone:
    """
    EN:
      Physical or logical zone in the vehicle.

    TR:
      Araçtaki fiziksel veya mantıksal zon.
    """
    name: str
    max_power_kw: float
    safety_level: Optional[str] = None


@dataclass
class ModuleType:
    """
    EN:
      Generic module definition from the library (capabilities, cost, limits).

    TR:
      Kütüphanedeki genel modül tanımı (yetkinlikler, maliyet, limitler).
    """
    id: str
    name: str
    cost: float
    max_power_kw: float
    supported_requirements: List[str] = field(default_factory=list)


@dataclass
class PlacedModule:
    """
    EN:
      A concrete instance of a module placed into a zone.

    TR:
      Bir zon içine yerleştirilmiş somut bir modül örneği.
    """
    module_type: ModuleType
    zone: Zone


@dataclass
class Link:
    """
    EN:
      Logical or physical connection between two placed modules.

    TR:
      İki yerleştirilmiş modül arasındaki mantıksal veya fiziksel bağlantı.
    """
    src: PlacedModule
    dst: PlacedModule
    medium: str  # e.g. "CAN", "Ethernet", "LIN"


@dataclass
class ArchitectureCandidate:
    """
    EN:
      A candidate zonal architecture configuration.

    TR:
      Aday bir zonal mimari konfigürasyonu.
    """
    zones: List[Zone]
    modules: List[PlacedModule]
    links: List[Link]
    score: Optional[float] = None