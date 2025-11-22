# ZAC – Architecture Overview  
*(English + Türkçe)*

---

# 1. Introduction / Giriş

**EN:**  
This document describes the high-level software architecture, data flow, and component responsibilities inside **ZAC (Zonal Architecture Compiler)**.  
ZAC converts vehicle-level functional requirements and a module library into optimized zonal E/E architectures.

**TR:**  
Bu doküman, **ZAC (Zonal Architecture Compiler)** içerisinde yer alan yüksek seviyeli yazılım mimarisini, veri akışını ve bileşen sorumluluklarını açıklar.  
ZAC, araç seviyesindeki fonksiyonel gereksinimleri ve modül kütüphanesini kullanarak optimize edilmiş zonal E/E mimarileri üretir.

---

# 2. System Goals / Sistem Hedefleri

**EN:**
- Reduce wiring complexity and total cable length  
- Provide modular, repeatable architecture generation  
- Enable cost-based, safety-based and redundancy-aware scoring  
- Allow OEMs to rapidly explore "what-if" architectural variations  
- Provide an extensible backend (Rust optimizers, ML heuristics, etc.)

**TR:**
- Kablolama karmaşıklığını ve toplam kablo uzunluğunu azaltmak  
- Tekrarlanabilir, modüler mimari üretimi yapmak  
- Maliyet, güvenlik ve yedeklilik odaklı puanlama sağlamak  
- OEM’lerin hızlı “what-if” analizleri yapmasını sağlamak  
- Genişletilebilir bir arka uç sağlamak (Rust optimizasyon motoru, ML heuristikleri vb.)

---

# 3. High-Level Architecture / Yüksek Seviye Mimari
+———————––+        +———————––+
|   requirements.json     |        |     modules.json        |
+————+————+        +————+————+
|                                 |
v                                 v
+———––+                 +––––––––+
|  loader.py  |  ————>  | ModuleLibrary  |
+———––+                 +––––––––+
|
v
+——————+
| RequirementSet   |
+——————+
|
v
+——————+
| generator.py     |
| (candidate gen.) |
+——————+
|
v
+——————+
| scorer.py        |
| (Rust backend)   |
+——————+
|
v
+——————————+
|  output architecture JSON    |
+——————————+
---

# 4. Data Model / Veri Modeli

ZAC’s internal model lives inside **`model.py`**.

## 4.1 Requirements / Gereksinimler

**EN:**  
Functional vehicle-level requirements (e.g. “Rear radar”, “Front Camera”, “ABS”).

**TR:**  
Araç seviyesinde fonksiyonel gereksinimler (“Arka radar”, “Ön kamera”, “ABS”).

Fields:
- `id` — unique requirement identifier  
- `zone_hint` — suggested physical zone  
- `safety_level` — ASIL rating (optional)

---

## 4.2 Zones / Zonlar

**EN:** Physical/functional region inside the vehicle.  
**TR:** Araçtaki fiziksel veya fonksiyonel bölge.

Fields:
- `name`
- `max_power_kw`
- `safety_level`

---

## 4.3 Module Library / Modül Kütüphanesi

Each module describes:
- cost  
- power consumption  
- capability list (which requirements it supports)

Module examples:
- Camera ECU  
- Sensor Fusion Unit  
- Power Distribution Node  
- Actuator Node  
- Gateway

---

## 4.4 Architecture Candidate

A candidate consists of:
- Set of zones  
- Placed modules (module + assigned zone)  
- Links (communication edges)  
- Computed scoring values

This enables rapid comparison between many architectural alternatives.

---

# 5. Compiler Pipeline / Derleyici Aşaması

## 5.1 loader.py — Input Parsing  
**EN:** Reads and validates JSON input files.  
**TR:** JSON giriş dosyalarını okur ve doğrular.

Output:
- `RequirementSet`
- `ModuleLibrary`

---

## 5.2 generator.py — Candidate Generation  
**EN:**  
Creates feasible architecture candidates. Early versions use simple deterministic rules.  
Later versions will include:
- Constraint-based placement  
- Graph search  
- Heuristics  
- Evolutionary algorithms

**TR:**  
Feasible mimari adayları üretir. İlk versiyon basit deterministik kurallar kullanır.  
Gelecek versiyonlarda:  
- Kısıt tabanlı yerleştirme  
- Grafik arama  
- Heuristik yöntemler  
- Evrimsel algoritmalar

---

## 5.3 scorer.py — Evaluation & Optimization  
**EN:**  
Computes a score for each candidate.  
Current implementation:  
- `score = -total_cost`

Future:
- Rust optimization engine  
- Multi-objective scoring  
- Wiring-length estimation  
- Safety penalties  
- Redundancy evaluation  
- Thermal constraints

**TR:**  
Her aday için skor hesaplar.  
Mevcut:  
- `score = -total_cost`

Gelecekte:  
- Rust optimizasyon motoru  
- Çoklu metrikli değerlendirme  
- Kablo uzunluğu tahmini  
- Güvenlik cezaları  
- Yedeklilik hesaplaması  
- Termal kısıtlar

---

# 6. Output / Üretilen Çıktı

**EN:**  
Final result is a JSON file containing:
- Zones  
- Placed modules  
- Communication links  
- Total cost  
- Total power  
- Score  
- Expandable fields for OEM reporting

**TR:**  
Üretilen çıktı bir JSON dosyasıdır ve şunları içerir:
- Zonlar  
- Yerleştirilmiş modüller  
- Haberleşme bağlantıları  
- Toplam maliyet  
- Toplam güç  
- Skor  
- OEM raporlama için genişletilebilir alanlar

---

# 7. Future Work / Gelecek Geliştirmeler

- Rust optimizer integration  
- Advanced constraint solver  
- Wiring length estimation engine  
- Multi-zone balancing algorithms  
- ML-based architecture recommendation  
- Automatic report generator (PDF/Word)

---

# 8. Summary / Özet

ZAC provides a structured, extensible, and professional workflow for generating zonal E/E architectures.  
As more components (Rust backend, heuristics, constraint solving) are integrated, ZAC will become a full-fledged OEM-grade decision-support tool.

ZAC, zonal E/E mimarileri üretmek için yapılandırılmış, genişletilebilir ve profesyonel bir akış sağlar. Rust arka ucu, heuristikler ve kısıt çözücü eklendikçe, ZAC OEM seviyesinde bir karar destek aracına dönüşecektir.