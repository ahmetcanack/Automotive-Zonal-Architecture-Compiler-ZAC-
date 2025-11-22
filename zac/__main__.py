"""
Entry point for `python -m zac`.

EN:
    This module allows running ZAC as a module:
        python -m zac ...

TR:
    Bu modül ZAC'in modül olarak çalıştırılmasını sağlar:
        python -m zac ...
"""

from .cli import main


if __name__ == "__main__":
    main()