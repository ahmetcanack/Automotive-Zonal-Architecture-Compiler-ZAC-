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
from typing import Dict, List, Optional, Tuple


# ---------- Zones / Zonlar ----------


@dataclass
class Zone:
    """
    EN:
        Physical or logical zone in the vehicle. Includes simple positional
        hints to roughly estimate harness length.

    TR:
        Araçtaki fiziksel veya mantıksal zon. Kablo uzunluğunu yaklaşık
        hesaplamak için basit konum ipuçları içerir.
    """

    name: str
    max_power_kw: float
    safety_level: Optional[str] = None  # e.g. "ASIL-B"
    latency_budget_ms: Optional[float] = None  # e.g. 10.0 ms end-to-end
    position: Optional[Tuple[float, float]] = None  # (x, y) meters in cabin plane


# ---------- Features / Requirements ----------


@dataclass
class Feature:
    """
    EN:
        Vehicle-level feature or requirement
        (e.g. "front camera", "ABS", "ADAS ECU").

    TR:
        Araç seviyesinde özellik veya gereksinim
        (örn. "ön kamera", "ABS", "ADAS ECU").
    """

    id: str
    name: str
    description: Optional[str] = None
    zone_hint: Optional[str] = None  # e.g. "Front-Left"
    zone_candidates: List[str] = field(default_factory=list)
    safety_level: Optional[str] = None  # e.g. "ASIL-B"
    latency_budget_ms: Optional[float] = None
    redundancy: int = 1  # desired instance count


@dataclass
class RequirementSet:
    """
    EN:
        Container for all features/requirements and zones of a vehicle.

    TR:
        Bir aracın tüm özellik/gereksinimlerini ve zonlarını tutan kapsayıcı.
    """

    vehicle_name: str
    zones: List["Zone"]
    features: List[Feature]


# ---------- Module library / Modül kütüphanesi ----------


@dataclass
class Module:
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
    supported_features: List[str] = field(default_factory=list)
    latency_class: Optional[str] = None  # e.g. "low", "medium", "high"
    zone_candidates: List[str] = field(default_factory=list)
    redundancy: int = 1
    notes: Optional[str] = None


@dataclass
class ModuleLibrary:
    """
    EN:
        All available module types that can be used in architectures.

    TR:
        Mimarilerde kullanılabilecek tüm modül tiplerini içerir.
    """

    modules: List[Module]

    def find_supporting_modules(self, feature_id: str) -> List[Module]:
        """
        EN:
            Return all module types that can support the given feature id.

        TR:
            Verilen özellik kimliğini destekleyebilen tüm modül
            tiplerini döndürür.
        """
        return [
            m for m in self.modules
            if feature_id in m.supported_features
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

    module: Module
    zone: Zone
    provided_features: List[str] = field(default_factory=list)


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
    bandwidth_mbps: Optional[float] = None
    latency_ms: Optional[float] = None
    length_m: Optional[float] = None
    redundant: bool = False


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
    penalties: Dict[str, float] = field(default_factory=dict)
    metrics: Dict[str, float] = field(default_factory=dict)

    @property
    def total_cost(self) -> float:
        """
        EN:
            Total hardware cost of all placed modules.

        TR:
            Yerleştirilen tüm modüllerin toplam donanım maliyeti.
        """
        return sum(pm.module.cost for pm in self.modules)

    @property
    def total_power_kw(self) -> float:
        """
        EN:
            Total power budget of all placed modules (rough).

        TR:
            Yerleştirilen tüm modüllerin yaklaşık toplam güç bütçesi.
        """
        return sum(pm.module.max_power_kw for pm in self.modules)

    @property
    def harness_length_m(self) -> float:
        """
        EN:
            Estimated harness length from link metadata if available.

        TR:
            Bağlantı metadatası varsa tahmini kablo uzunluğu.
        """
        lengths = [l.length_m for l in self.links if l.length_m is not None]
        return sum(lengths)
