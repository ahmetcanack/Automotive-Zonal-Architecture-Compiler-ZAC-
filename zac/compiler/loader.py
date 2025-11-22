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


# --- Expected JSON formats / Beklenen JSON formatları ---
#
# requirements.json
# -----------------
# {
#   "vehicle": {
#     "name": "Demo Car",
#     "zones": [
#       {"name": "Front-Left", "max_power_kw": 2.5, "safety_level": "ASIL-B"},
#       {"name": "Rear",        "max_power_kw": 2.0}
#     ]
#   },
#   "requirements": [
#     {"id": "REQ_CAM_F", "name": "Front camera", "zone_hint": "Front-Left",
#      "safety_level": "ASIL-B"}
#   ]
# }
#
# modules.json
# ------------
# {
#   "modules": [
#     {
#       "id": "MOD_CAM_ECU",
#       "name": "Camera ECU",
#       "cost": 50.0,
#       "max_power_kw": 0.2,
#       "supported_requirements": ["REQ_CAM_F"]
#     }
#   ]
# }


def _read_json(path: Path) -> Dict[str, Any]:
    """
    EN:
        Read a JSON file and return the parsed object.

    TR:
        Bir JSON dosyasını okuyup parse edilmiş objeyi döndürür.
    """
    return json.loads(path.read_text(encoding="utf-8"))


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
    vehicle_name = str(vehicle.get("name", "Unnamed vehicle"))

    # Zones
    zones_data = vehicle.get("zones", [])
    zones: List[model.Zone] = []
    for z in zones_data:
        zones.append(
            model.Zone(
                name=str(z["name"]),
                max_power_kw=float(z.get("max_power_kw", 0.0)),
                safety_level=z.get("safety_level"),
            )
        )

    # Requirements
    reqs_data = data.get("requirements", [])
    reqs: List[model.Requirement] = []
    for r in reqs_data:
        reqs.append(
            model.Requirement(
                id=str(r["id"]),
                name=str(r.get("name", r["id"])),
                zone_hint=r.get("zone_hint"),
                safety_level=r.get("safety_level"),
            )
        )

    return model.RequirementSet(
        vehicle_name=vehicle_name,
        zones=zones,
        requirements=reqs,
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

    modules: List[model.ModuleType] = []
    for m in modules_data:
        modules.append(
            model.ModuleType(
                id=str(m["id"]),
                name=str(m.get("name", m["id"])),
                cost=float(m.get("cost", 0.0)),
                max_power_kw=float(m.get("max_power_kw", 0.0)),
                supported_requirements=list(m.get("supported_requirements", [])),
            )
        )

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
        "zones": [
            {
                "name": z.name,
                "max_power_kw": z.max_power_kw,
                "safety_level": z.safety_level,
            }
            for z in candidate.zones
        ],
        "modules": [
            {
                "type_id": pm.module_type.id,
                "type_name": pm.module_type.name,
                "zone": pm.zone.name,
                "cost": pm.module_type.cost,
                "max_power_kw": pm.module_type.max_power_kw,
            }
            for pm in candidate.modules
        ],
        "links": [
            {
                "src": link.src.module_type.id,
                "dst": link.dst.module_type.id,
                "medium": link.medium,
            }
            for link in candidate.links
        ],
        "score": candidate.score,
        "total_cost": candidate.total_cost,
        "total_power_kw": candidate.total_power_kw,
    }

    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")