import sys
path = 'home/rojq12/FactorioSaveApi'
if path not in sys.path:
   sys.path.insert(0, path)

from main import app as application