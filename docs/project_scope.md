# ZAC – Project Scope & Intent  
*(English + Türkçe)*

---

## 1. High-Level Goal / Yüksek Seviye Amaç

**EN:**  
ZAC (**Zonal Architecture Compiler**), otomotiv E/E sistemleri için **zonal mimari tasarımı** yapan bir derleyicidir.  
Temel amacı:

- Vehicle-level **functional requirements** (JSON)
- Pre-defined **module library** (JSON)

girdilerini alıp, **feasible zonal E/E architecture candidates** üretmek, bunları maliyet/güç vb. metriklere göre **skorlamak** ve en iyi adayı JSON olarak çıkarmaktır.

**TR:**  
ZAC (**Zonal Architecture Compiler**), otomotiv E/E sistemlerinde **zonal mimari tasarımı** yapan bir derleyicidir.  
Amacı:

- Araç seviyesinde **fonksiyonel gereksinimleri** (JSON)
- Önceden tanımlanmış **modül kütüphanesini** (JSON)

girdi olarak alıp, **feasible zonal E/E mimari adayları** üretmek, bu adayları maliyet/güç vb. metriklere göre **puanlamak** ve en iyi adayı JSON olarak çıktıya vermektir.

---

## 2. In-Scope / Kapsam Dahilinde

**EN:**

- Taking **requirements.json** and **modules.json** as inputs
- Building internal models (`RequirementSet`, `ModuleLibrary`, `ArchitectureCandidate`)
- Distributing modules into zones based on:
  - `zone_hint`
  - power budget (`max_power_kw`)
  - requirement coverage
- Generating **candidate architectures**
- **Scoring** candidates (cost-based for now, extensible later)
- **Selecting** and **exporting** the best candidate as JSON
- Having a **stable CLI** (`zac`) that can be integrated into toolchains and CI

**TR:**

- **requirements.json** ve **modules.json** dosyalarını girdi olarak almak
- Dahili modelleri oluşturmak (`RequirementSet`, `ModuleLibrary`, `ArchitectureCandidate`)
- Modülleri zonlara yerleştirmek:
  - `zone_hint`
  - güç bütçesi (`max_power_kw`)
  - gereksinim karşılama durumuna göre
- **Mimari adayları** üretmek
- Adayları **skorlamak** (şimdilik maliyet tabanlı, ileride genişletilebilir)
- En iyi adayı **seçmek** ve JSON olarak **export** etmek
- Araç zincirlerine ve CI’a entegre edilebilecek **stabil bir CLI** (`zac`) sunmak

---

## 3. Out-of-Scope / Kapsam Dışı

**EN:**

- Low-level ECU firmware implementation
- Detailed physical wiring harness design
- 3D packaging / CAD
- Real-time scheduling, AUTOSAR stack implementation
- Safety case documentation (ISO 26262 work products)

**TR:**

- Düşük seviye ECU firmware implementasyonu
- Detaylı fiziksel kablo demeti (wiring harness) tasarımı
- 3D paketleme / CAD
- Gerçek zamanlı task schedule’ı, AUTOSAR stack implementasyonu
- ISO 26262 kapsamındaki safety dokümantasyonu

---

## 4. Pipeline Overview / Derleyici Hattı

```text
requirements.json        modules.json
        |                     |
        v                     v
    loader.py            loader.py
        |                     |
        +------> RequirementSet
                          +
                     ModuleLibrary
                          |
                          v
                     generator.py
                          |
                          v
                      candidates
                          |
                          v
                      scorer.py
                          |
                          v
                best ArchitectureCandidate
                          |
                          v
                    output JSON (architecture)

EN (summary):
	1.	loader.py
	•	Reads JSON
	•	Builds RequirementSet and ModuleLibrary
	2.	generator.py
	•	Produces feasible architecture candidates
	3.	scorer.py
	•	Scores candidates (cost-based for now, Rust optimizer later)
	4.	loader.dump_architecture()
	•	Writes selected architecture as JSON

TR (özet):
	1.	loader.py
	•	JSON’ları okur
	•	RequirementSet ve ModuleLibrary objelerini oluşturur
	2.	generator.py
	•	Feasible mimari adayları üretir
	3.	scorer.py
	•	Adayları skorlar (şimdilik maliyet tabanlı, ileride Rust optimizer)
	4.	loader.dump_architecture()
	•	Seçilen mimariyi JSON olarak yazar

⸻

5. CLI Contract / CLI Sözleşmesi

EN:
	•	The only official entrypoint is the zac CLI.
	•	Python entrypoint:
	•	python -m zac ... → goes to zac/__main__.py → zac.cli.main()
	•	Console script entrypoint:
	•	zac = "zac.cli:main" (see pyproject.toml)

Current CLI:
zac \
  --requirements examples/sample_requirements.json \
  --modules examples/sample_modules.json \
  --output out.json
  Arguments (MUST stay stable):
	•	--requirements PATH → Requirements JSON input
	•	--modules PATH → Module library JSON input
	•	--output PATH → Output architecture JSON

TR:
	•	Tek resmi giriş noktası zac CLI’dir.
	•	Python entrypoint:
	•	python -m zac ... → zac/__main__.py → zac.cli.main()
	•	Console script entrypoint:
	•	zac = "zac.cli:main" (pyproject.toml içinde)

Mevcut CLI:
zac \
  --requirements examples/sample_requirements.json \
  --modules examples/sample_modules.json \
  --output out.json

  Argümanlar (değiştirilmemelidir):
	•	--requirements PATH → Gereksinim JSON girişi
	•	--modules PATH → Modül kütüphanesi JSON girişi
	•	--output PATH → Çıktı mimarisi JSON

AI için kural: CLI argüman imzasını rastgele değiştirme.
Gerekirse yeni seçenekler opsiyonel flag olarak eklenebilir, mevcut argümanlar bozulmamalıdır.

⸻

6. Data Model Constraints / Veri Modeli Kısıtları

Requirements & Zones
	•	Every requirement has:
	•	id: str
	•	name: str
	•	zone_hint: Optional[str]
	•	safety_level: Optional[str]
	•	Every zone has:
	•	name: str
	•	max_power_kw: float
	•	safety_level: Optional[str]

Modules
	•	Every module type has:
	•	id: str
	•	name: str
	•	cost: float
	•	max_power_kw: float
	•	supported_requirements: List[str]

ArchitectureCandidate
	•	Consists of:
	•	zones: List[Zone]
	•	modules: List[PlacedModule]
	•	links: List[Link] (currently empty, reserved for future networking model)
	•	score: Optional[float]

TR Özet:
	•	Gereksinimler (requirements) → zorunlu id, opsiyonel zone_hint, safety_level
	•	Zonlar (zones) → güç bütçesi (max_power_kw) ve opsiyonel safety seviyesi içerir
	•	Modüller → cost, max_power_kw, hangi gereksinimleri desteklediği (supported_requirements)
	•	Mimari adayı → zonlar + yerleştirilmiş modüller + bağlantılar + skor

⸻

7. Current Simplifications / Mevcut Basitleştirmeler

EN:
	•	Generator uses a naive strategy:
	•	For each requirement:
	•	Pick the first module that supports it
	•	Place into zone_hint if available, else first zone
	•	No power balancing, safety constraints or wiring length yet
	•	Scorer:
	•	score = -total_cost
	•	No multi-objective optimization yet

TR:
	•	Generator şu an çok basit bir strateji kullanır:
	•	Her gereksinim için:
	•	Onu destekleyen ilk modülü seçer
	•	Varsa zone_hint zonuna, yoksa ilk zon’a yerleştirir
	•	Güç dengesi, güvenlik kısıtları, kablo uzunluğu vs. şimdilik yok
	•	Scorer:
	•	score = -total_cost
	•	Henüz çoklu metrikli optimizasyon yok

AI’ye Not:
Mevcut davranışı bozmadan, yeni algoritmalar genişleme şeklinde eklenmelidir.
Örn: generator_v2, advanced_scorer gibi yeni fonksiyonlar; generator.generate_candidates imzası kırılmamalıdır.

⸻

8. Future Directions / Gelecek Yönü

Planlanan genişlemeler:
	•	Rust-tabancı optimizer (optimizer_rs) entegrasyonu
	•	Multi-objective scoring:
	•	Cost
	•	Power balance
	•	Wiring length (approx.)
	•	Safety & redundancy
	•	Network topology generation (graph/):
	•	CAN / LIN / Ethernet link modelling
	•	Constraint solver integration
	•	OEM-grade reporting (HTML/PDF summaries)

9. Guidelines for AI Assistants / AI Asistanları için Kurallar

EN (for any AI tool working on this repo):
	1.	Always read this file (docs/project_scope.md) and docs/architecture.md before making significant changes.
	2.	Do NOT change the CLI signature:
	•	Keep --requirements, --modules, --output as they are.
	3.	Do NOT rename core modules:
	•	zac/cli/, zac/compiler/, zac/__main__.py
	4.	Prefer adding new modules/functions over breaking existing ones.
	5.	When modifying logic:
	•	Keep docstrings bilingual (EN + TR).
	•	Preserve existing behavior unless explicitly requested otherwise.
	6.	Never introduce framework-specific dependencies (FastAPI, Django, etc.) into the core compiler.

TR (bu repoda çalışan tüm AI araçları için):
	1.	Önemli bir değişiklik yapmadan önce bu dosyayı (docs/project_scope.md) ve docs/architecture.md’yi oku.
	2.	CLI imzasını değiştirme:
	•	--requirements, --modules, --output olduğu gibi kalmalı.
	3.	Çekirdek modülleri yeniden adlandırma:
	•	zac/cli/, zac/compiler/, zac/__main__.py
	4.	Mevcut fonksiyonları kırmak yerine, yeni fonksiyon/modül eklemeyi tercih et.
	5.	Mantık değiştiriyorsan:
	•	Docstring’leri EN+TR koru.
	•	Davranışı, özellikle kullanıcı akışını, açık istek yoksa bozma.
	6.	Çekirdek derleyiciye framework bağımlılığı ekleme (FastAPI, Django vb.).

⸻

10. Short Summary / Kısa Özet

EN:
ZAC is a zonal architecture compiler: it goes from requirements + module library → candidate architectures → scoring → best architecture JSON. The CLI, data model, and directory layout are considered stable contracts and should not be broken.

TR:
ZAC bir zonal mimari derleyicisidir: gereksinimler + modül kütüphanesinden → mimari adayları → skor → en iyi mimari JSON çıktısına gider. CLI, veri modeli ve dizin yapısı stabil sözleşme olarak kabul edilir ve rastgele bozulmamalıdır.