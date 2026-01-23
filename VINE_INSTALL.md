# Vine Copula Installation

The R-vine copula module (`pyreto.vine`) requires `pyvinecop` which is a C++ backend accessed via ctypes.

## Installation

```bash
pip install pyvinecop
```

Or if using the virtual environment:
```bash
source .venv/bin/activate
.venv/bin/pip install pyvinecop
```

## Verify Installation

```bash
python -c "import pyvinecop; print('pyvinecop', pyvinecop.__version__)"
```

## Fallback Behavior

If pyvinecop is not installed, the module will raise an `ImportError` with clear instructions when any vine function is called:

```python
import pyreto as pr

# This will raise ImportError if pyvinecop not installed
try:
    vine = pr.vine.fit(data, family_set=["gumbel", "t"])
except ImportError as e:
    print(e)  # "pyvinecop not installed. Run: pip install pyvinecop"
```

## Platform Support

pyvinecop provides pre-built wheels for:
- Linux (x86_64, manylinux)
- macOS (Intel and Apple Silicon)
- Windows (64-bit)

For other platforms, compilation from source is required (needs C++11 compiler).
