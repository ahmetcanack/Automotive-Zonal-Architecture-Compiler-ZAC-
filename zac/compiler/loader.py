"""
Loading and dumping utilities for ZAC JSON files.

EN:
    Responsible for reading JSON inputs and writing JSON outputs.

TR:
    JSON girişlerini okuyan ve JSON çıktıları yazan yardımcı
    fonksiyonları içerir.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from . import model


def _read_json(path: Path) -> Dict[str, Any]:
    """
    EN:
        Read a JSON file and return the parsed object.

    TR:
        Bir JSON dosyasını okuyup parse edilmiş objeyi döndürür.
    """
    return json.loads(path.read_text(encoding="utf-8"))


def _parse_zone(zone_data: Dict[str, Any]) -> model.Zone:
    if "name" not in zone_data:
        raise ValueError("Zone is missing required field 'name'.")
    if "max_power_kw" not in zone_data:
        raise ValueError(f"Zone '{zone_data.get('name', 'unknown')}' is missing 'max_power_kw'.")

    position = None
    if isinstance(zone_data.get("position"), dict):
        pos_data = zone_data["position"]
        if "x" in pos_data and "y" in pos_data:
            position = (float(pos_data["x"]), float(pos_data["y"]))
        else:
            raise ValueError(f"Zone '{zone_data['name']}' position must include x and y.")

    return model.Zone(
        name=str(zone_data["name"]),
        max_power_kw=float(zone_data["max_power_kw"]),
        safety_level=zone_data.get("safety_level"),
        latency_budget_ms=(
            float(zone_data["latency_budget_ms"])
            if "latency_budget_ms" in zone_data else None
        ),
        position=position,
    )


def _parse_feature(feature_data: Dict[str, Any]) -> model.Feature:
    if "id" not in feature_data:
        raise ValueError("Feature/Requirement entry is missing 'id'.")

    zone_candidates = feature_data.get("zone_candidates") or []
    if not isinstance(zone_candidates, list):
        raise ValueError(f"Feature '{feature_data['id']}' zone_candidates must be a list.")

    redundancy = feature_data.get("redundancy", 1)
    try:
        redundancy_val = int(redundancy)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Feature '{feature_data['id']}' redundancy must be an integer.") from exc

    return model.Feature(
        id=str(feature_data["id"]),
        name=str(feature_data.get("name", feature_data["id"])),
        description=feature_data.get("description"),
        zone_hint=feature_data.get("zone_hint"),
        zone_candidates=[str(z) for z in zone_candidates],
        safety_level=feature_data.get("safety_level"),
        latency_budget_ms=(
            float(feature_data["latency_budget_ms"])
            if "latency_budget_ms" in feature_data else None
        ),
        redundancy=redundancy_val,
    )


def _parse_module(module_data: Dict[str, Any]) -> model.Module:
    if "id" not in module_data:
        raise ValueError("Module entry is missing 'id'.")
    if "cost" not in module_data:
        raise ValueError(f"Module '{module_data.get('id', 'unknown')}' is missing 'cost'.")
    if "max_power_kw" not in module_data:
        raise ValueError(f"Module '{module_data.get('id', 'unknown')}' is missing 'max_power_kw'.")

    supported = module_data.get("supported_features") or module_data.get("supported_requirements") or []
    if not isinstance(supported, list):
        raise ValueError(f"Module '{module_data['id']}' supported_features must be a list.")

    zone_candidates = module_data.get("zone_candidates") or []
    if not isinstance(zone_candidates, list):
        raise ValueError(f"Module '{module_data['id']}' zone_candidates must be a list.")

    redundancy = module_data.get("redundancy", 1)
    try:
        redundancy_val = int(redundancy)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Module '{module_data['id']}' redundancy must be an integer.") from exc

    return model.Module(
        id=str(module_data["id"]),
        name=str(module_data.get("name", module_data["id"])),
        cost=float(module_data["cost"]),
        max_power_kw=float(module_data["max_power_kw"]),
        supported_features=[str(s) for s in supported],
        latency_class=module_data.get("latency_class"),
        zone_candidates=[str(z) for z in zone_candidates],
        redundancy=redundancy_val,
        notes=module_data.get("notes"),
    )


# ---------- Requirements ----------


def load_requirements(path: Path) -> model.RequirementSet:
    """
    EN:
        Load requirements from JSON file and convert to internal structures.

    TR:
        Gereksinimleri JSON dosyasından okuyup dahili yapılara çevirir.
    """
    data = _read_json(path)

    vehicle = data.get("vehicle", {})
    zones_data = data.get("zones") or vehicle.get("zones") or []
    if not zones_data:
        raise ValueError("No zones provided in requirements JSON.")

    zones: List[model.Zone] = [_parse_zone(z) for z in zones_data]

    features_data = data.get("features") or data.get("requirements") or []
    if not features_data:
        raise ValueError("No features/requirements provided in requirements JSON.")

    features: List[model.Feature] = [_parse_feature(f) for f in features_data]

    vehicle_name = str(vehicle.get("name", data.get("vehicle_name", "Unnamed vehicle")))

    return model.RequirementSet(
        vehicle_name=vehicle_name,
        zones=zones,
        features=features,
    )


# ---------- Module library ----------


def load_module_library(path: Path) -> model.ModuleLibrary:
    """
    EN:
        Load module library from JSON file.

    TR:
        Modül kütüphanesini JSON dosyasından yükler.
    """
    data = _read_json(path)
    modules_data = data.get("modules", [])

    if not modules_data:
        raise ValueError("Module library JSON must include a 'modules' array.")

    modules: List[model.Module] = [_parse_module(m) for m in modules_data]

    return model.ModuleLibrary(modules=modules)


# ---------- Output architecture JSON ----------


def dump_architecture(candidate: model.ArchitectureCandidate, path: Path) -> None:
    """
    EN:
        Serialize selected architecture into JSON.

    TR:
        Seçilen mimariyi JSON formatında dosyaya yazar.
    """
    payload: Dict[str, Any] = {
        "vehicle": {
            "zones": [
                {
                    "name": z.name,
                    "max_power_kw": z.max_power_kw,
                    "safety_level": z.safety_level,
                    "latency_budget_ms": z.latency_budget_ms,
                    "position": {"x": z.position[0], "y": z.position[1]} if z.position else None,
                }
                for z in candidate.zones
            ]
        },
        "architecture": {
            "modules": [
                {
                    "type_id": pm.module.id,
                    "type_name": pm.module.name,
                    "zone": pm.zone.name,
                    "cost": pm.module.cost,
                    "max_power_kw": pm.module.max_power_kw,
                    "supported_features": pm.module.supported_features,
                    "provided_features": pm.provided_features,
                }
                for pm in candidate.modules
            ],
            "links": [
                {
                    "src": link.src.module.id,
                    "dst": link.dst.module.id,
                    "medium": link.medium,
                    "bandwidth_mbps": link.bandwidth_mbps,
                    "latency_ms": link.latency_ms,
                    "length_m": link.length_m,
                    "redundant": link.redundant,
                }
                for link in candidate.links
            ],
        },
        "score": candidate.score,
        "penalties": candidate.penalties,
        "metrics": {
            "total_cost": candidate.total_cost,
            "total_power_kw": candidate.total_power_kw,
            "harness_length_m": candidate.harness_length_m,
        },
    }

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
