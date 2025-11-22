"""
ZAC optimizer Python wrapper.

Buradan Rust'taki optimizer_core modülünü kullanacağız.
Şimdilik sadece add_numbers fonksiyonunu expose ediyoruz.
"""

try:
    import optimizer_core  # Rust modülü (maturin develop ile gelmişti)
except ImportError:
    optimizer_core = None


def add(a: int, b: int) -> int:
    """
    Simple test wrapper around Rust's add_numbers.
    """
    if optimizer_core is None:
        raise RuntimeError(
            "optimizer_core not available. Did you run `maturin develop`?"
        )
    return optimizer_core.add_numbers(a, b)