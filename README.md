# ZAC – Zonal Architecture Compiler  
*(English + Türkçe)*  
Author: Ahmet Can Kuğuoğlu

---

# 📌 Overview / Genel Bakış

**EN:**  
ZAC (Zonal Architecture Compiler) reads vehicle-level requirements and a module library (JSON) and produces zonal E/E architecture candidates. Current version uses a simple Python-only pipeline (no Rust optimizer yet): it picks the first supporting module per requirement, places by `zone_hint` (or first zone), and scores by total cost (`score = -total_cost`).

**TR:**  
ZAC (Zonal Architecture Compiler) araç gereksinimleri ve modül kütüphanesini (JSON) okuyup zonal E/E mimari adayları üretir. Mevcut sürüm sadece Python kullanır (Rust optimizer yok): her gereksinim için ilk destekleyen modülü seçer, `zone_hint` varsa o zonda (yoksa ilk zonda) yerleştirir, skoru toplam maliyete göre hesaplar (`score = -total_cost`).

> Ayrıntılı kapsam ve kurallar için `docs/project_scope.md` ve `docs/architecture.md` dosyalarına bakın.

---

# 🎯 Purpose & Current State / Amaç ve Mevcut Durum

**EN:**  
Goal: standardize and automate zonal architecture design while keeping the CLI stable.

- Inputs: `requirements.json`, `modules.json`
- Models: `RequirementSet`, `ModuleLibrary`, `ArchitectureCandidate`
- Generation: naive first-match placement, no power/safety balancing yet
- Scoring: cost only (`score = -total_cost`)
- Output: best candidate as JSON

**TR:**  
Amaç: zonal mimari tasarımını standartlaştırmak ve otomatikleştirmek, CLI sabit kalsın.

- Girdiler: `requirements.json`, `modules.json`
- Modeller: `RequirementSet`, `ModuleLibrary`, `ArchitectureCandidate`
- Üretim: ilk uyumlu modülü seçip yerleştirir, güç/güvenlik dengesi yok
- Skorlama: sadece maliyet (`score = -total_cost`)
- Çıktı: en iyi aday JSON

---

# 🧱 Project Structure / Proje Yapısı

```text
zac/
├── docs/
│   ├── architecture.md
│   └── project_scope.md
├── examples/
│   ├── sample_modules.json
│   └── sample_requirements.json
├── zac/
│   ├── cli/
│   │   └── __init__.py
│   ├── compiler/
│   │   ├── generator.py
│   │   ├── loader.py
│   │   ├── model.py
│   │   └── scorer.py
│   ├── core/
│   ├── graph/
│   ├── optimizer/
│   │   └── optimizer_core/ (Rust stub)
│   ├── __init__.py
│   └── __main__.py
├── main.py
├── pyproject.toml
└── README.md
```

---

# 🚀 Usage / Kullanım

CLI sözleşmesi sabittir (değiştirilmemelidir):

```bash
zac \
  --requirements examples/sample_requirements.json \
  --modules examples/sample_modules.json \
  --output out.json
```

- `--requirements PATH` → Requirements JSON input  
- `--modules PATH` → Module library JSON input  
- `--output PATH` → Output architecture JSON  

Alternatif giriş noktaları: `python -m zac ...` veya `python main.py ...` (aynı argümanlar).

---

# 📂 Inputs & Output / Girdiler ve Çıktı

**requirements.json**  
- `vehicle.name` (string)  
- `vehicle.zones[]` → `name`, `max_power_kw`, `safety_level?`  
- `requirements[]` → `id`, `name?`, `zone_hint?`, `safety_level?`

**modules.json**  
- `modules[]` → `id`, `name?`, `cost`, `max_power_kw`, `supported_requirements[]`

**Output JSON** (örnek `out.json`)  
- `zones[]`, `modules[]` (type, zone, cost, power), `links[]` (şimdilik boş), `score`, `total_cost`, `total_power_kw`

Örnekler için `examples/sample_requirements.json` ve `examples/sample_modules.json` dosyalarına bakın.

---

# 🛠 Status & Roadmap / Durum ve Yol Haritası

- ✅ Naive candidate generator (ilk destekleyen modül, `zone_hint` ile yerleştirme)  
- ✅ Cost-based scorer (`score = -total_cost`)  
- ✅ Stabil CLI: `zac --requirements --modules --output`
- ⚠️ Güç/safety dengesi, kablo uzunluğu, çoklu aday üretimi yok (mevcut basitleştirme)  
- ⚙️ Rust optimizer stub (`zac/optimizer/optimizer_core`), entegrasyon henüz yok

---

# 🤝 Contributing / Katkı

- CLI argümanları sabit kalmalı (`--requirements`, `--modules`, `--output`).  
- Çekirdek yollar yeniden adlandırılmamalı (`zac/cli`, `zac/compiler`, `zac/__main__.py`).  
- Davranış geri uyumlu genişletmeler tercih edilmeli (örn. `generator_v2` eklemek).  
- Docstring’ler EN+TR korunmalı.  
- Framework bağımlılığı eklemeyin (FastAPI, Django vb.) çekirdek derleyiciye.
