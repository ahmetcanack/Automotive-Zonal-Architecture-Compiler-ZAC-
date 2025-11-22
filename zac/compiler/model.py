"""
Core data models for ZAC.

EN:
    Defines the internal representation of requirements, zones,
    modules, links and architecture candidates.

TR:
    Gereksinimler, zonlar, modüller, bağlantılar ve mimari adayları için
    ZAC'in dahili veri modellerini tanımlar.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


# ---------- Requirements / Gereksinimler ----------


@dataclass
class Requirement:
    """
    EN:
        High-level vehicle requirement
        (e.g. "front camera", "ABS", "ADAS ECU").

    TR:
        Yüksek seviyeli araç gereksinimi
        (örn. "ön kamera", "ABS", "ADAS ECU").
    """

    id: str
    name: str
    zone_hint: Optional[str] = None  # e.g. "Front-Left"
    safety_level: Optional[str] = None  # e.g. "ASIL-B"


@dataclass
class RequirementSet:
    """
    EN:
        Container for all requirements and zones of a vehicle.

    TR:
        Bir aracın tüm gereksinimlerini ve zonlarını tutan kapsayıcı.
    """

    vehicle_name: str
    zones: List["Zone"]
    requirements: List[Requirement]


# ---------- Zones / Zonlar ----------


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


# ---------- Module library / Modül kütüphanesi ----------


@dataclass
class ModuleType:
    """
    EN:
        Generic module definition from the library
        (capabilities, cost, limits).

    TR:
        Kütüphanedeki genel modül tanımı
        (yetkinlikler, maliyet, limitler).
    """

    id: str
    name: str
    cost: float
    max_power_kw: float
    supported_requirements: List[str] = field(default_factory=list)


@dataclass
class ModuleLibrary:
    """
    EN:
        All available module types that can be used in architectures.

    TR:
        Mimarilerde kullanılabilecek tüm modül tiplerini içerir.
    """

    modules: List[ModuleType]

    def find_supporting_modules(self, requirement_id: str) -> List[ModuleType]:
        """
        EN:
            Return all module types that can support the given requirement id.

        TR:
            Verilen gereksinim kimliğini destekleyebilen tüm modül
            tiplerini döndürür.
        """
        return [
            m for m in self.modules
            if requirement_id in m.supported_requirements
        ]


# ---------- Concrete architecture / Somut mimari ----------


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

    @property
    def total_cost(self) -> float:
        """
        EN:
            Total hardware cost of all placed modules.

        TR:
            Yerleştirilen tüm modüllerin toplam donanım maliyeti.
        """
        return sum(pm.module_type.cost for pm in self.modules)

    @property
    def total_power_kw(self) -> float:
        """
        EN:
            Total power budget of all placed modules (rough).

        TR:
            Yerleştirilen tüm modüllerin yaklaşık toplam güç bütçesi.
        """
        return sum(pm.module_type.max_power_kw for pm in self.modules)