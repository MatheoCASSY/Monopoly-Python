import importlib.util
import sys
from pathlib import Path

main_path = Path(__file__).parent.parent / 'Scripts-Python' / 'Main.py'
if not main_path.exists():
    print('Main.py not found at', main_path)
    sys.exit(1)

spec = importlib.util.spec_from_file_location('main_module', str(main_path))
mod = importlib.util.module_from_spec(spec)
sys.modules['main_module'] = mod
# Ensure the Scripts-Python directory is on sys.path so local imports resolve
sys.path.insert(0, str(main_path.parent))
spec.loader.exec_module(mod)

# Call the simuler_parties function with a small test
print('\n=== Running quick simulation test (3 parties, 4 joueurs) ===')
mod.simuler_parties(3, 4, None)
print('\n=== Test completed ===')
