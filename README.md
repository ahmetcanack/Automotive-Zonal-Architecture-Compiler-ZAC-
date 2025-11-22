# ZAC – Zonal Architecture Compiler  
*(English + Türkçe)*

---

# 📌 Overview / Genel Bakış

**EN:**  
ZAC (Zonal Architecture Compiler) is a tooling framework that takes vehicle-level requirements and module libraries as input, and automatically generates optimized zonal E/E architectures. It aims to help OEMs and suppliers evaluate different topology candidates, minimize wiring complexity, reduce cost, and meet safety & redundancy constraints.

**TR:**  
ZAC (Zonal Architecture Compiler), araç seviyesindeki gereksinimleri ve modül kütüphanelerini girdi olarak alıp, otomatik olarak optimize edilmiş zonal E/E mimarileri üreten bir çerçevedir. OEM’lerin ve tedarikçilerin farklı topoloji adaylarını değerlendirmesine, kablo karmaşıklığını ve maliyeti azaltmasına, güvenlik ve yedeklilik kurallarını sağlamasına yardımcı olur.

---

# 🎯 Purpose & Goals / Amaç ve Hedefler

**EN:**  
The goal of ZAC is to standardize and automate the design process of modern zonal vehicle architectures by:

- Converting raw requirements into a formal internal model  
- Generating possible zonal topologies  
- Scoring them through a Rust-based optimization engine  
- Selecting the best candidates according to cost, wiring length, safety, and power constraints  

**TR:**  
ZAC'in amacı modern zonal araç mimarilerinin tasarım sürecini standartlaştırmak ve otomatikleştirmektir:

- Ham gereksinimleri iç modelimize dönüştürmek  
- Olası zonal topolojileri üretmek  
- Bu topolojileri Rust tabanlı bir optimize ediciyle puanlamak  
- Maliyet, kablo uzunluğu, güvenlik ve güç limitlerine göre en iyi adayları seçmek

---

# 🧱 Project Structure / Proje Yapısı

```text
Automotive-Zonal-Architecture-Compiler-ZAC-/
├── docs/
│   └── architecture.md
│
├── examples/
│   ├── sample_modules.json
│   └── sample_requirements.json
│
├── zac/
│   ├── cli/
│   │   └── __init__.py
│   │
│   ├── compiler/
│   │   ├── generator.py
│   │   ├── loader.py
│   │   ├── model.py
│   │   └── scorer.py
│   │
│   ├── core/
│   ├── graph/
│   ├── optimizer/
│   │
│   ├── __init__.py
│   └── __main__.py
│
├── .gitignore
├── README.md
├── main.py
└── pyproject.toml