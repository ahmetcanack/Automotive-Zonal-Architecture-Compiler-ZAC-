"""
Loading and dumping utilities for ZAC JSON files.

EN:
  Responsible for reading JSON inputs and writing JSON outputs.

TR:
  JSON girişlerini okuyan ve JSON çıktıları yazan yardımcı fonksiyonları içerir.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from . import model


def load_requirements(path: Path) -> Any:
    """
    EN:
      Load requirements from JSON file and convert to internal structures.

    TR:
      Gereksinimleri JSON dosyasından okuyup dahili yapılara çevirir.
    """
    data = json.loads(path.read_text(encoding="utf-8"))
    # TODO: Real parsing → Requirement / Zone nesneleri.
    return data


def load_module_library(path: Path) -> Any:
    """
    EN:
      Load module library from JSON file.

    TR:
      Modül kütüphanesini JSON dosyasından yükler.
    """
    data = json.loads(path.read_text(encoding="utf-8"))
    # TODO: Real parsing → ModuleType nesneleri.
    return data


def dump_architecture(candidate: model.ArchitectureCandidate, path: Path) -> None:
    """
    EN:
      Serialize selected architecture into JSON.

    TR:
      Seçilen mimariyi JSON formatında dosyaya yazar.
    """
    payload: Dict[str, Any] = {
        "zones": [z.name for z in candidate.zones],
        "modules": [pm.module_type.name for pm in candidate.modules],
        "links": [
            {
                "src": pm.src.module_type.name,
                "dst": pm.dst.module_type.name,
                "medium": pm.medium,
            }
            for pm in candidate.links
        ],
        "score": candidate.score,
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")