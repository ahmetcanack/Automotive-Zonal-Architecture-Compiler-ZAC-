"""
Entry point for `python -m zac`.

EN:
    Allows running ZAC as a module:
        python -m zac ...

TR:
    ZAC'i modül olarak çalıştırmanızı sağlar:
        python -m zac ...
"""

from .cli import main


if __name__ == "__main__":
    main()