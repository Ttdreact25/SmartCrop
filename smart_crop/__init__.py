# Makes 'smart_crop' folder a Python module (renamed from 'src' to avoid conflicts)
# Note: Do not import submodules here to avoid namespace collision with system packages

# expose leaf detection helpers at package level (optional)
from .leaf_detector import load_leaf_model, predict_leaf