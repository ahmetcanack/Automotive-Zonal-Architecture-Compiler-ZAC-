"""
Compiler subsystem for ZAC.

EN:
  Contains code that loads input data, builds internal models,
  generates candidate architectures and interfaces with the optimizer.

TR:
  Girdi verilerini yükleyen, iç modelleri kuran, mimari adayları üreten
  ve optimize edici ile konuşan derleyici alt sistemini içerir.
"""

from . import loader, model, generator, scorer  # noqa: F401