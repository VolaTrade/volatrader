import importlib

def get_strategy(class_: str)->object:
    cls_path: str = "src.strategies." + class_ + "." + class_
    parts = cls_path.split('.')
    module = ".".join(parts[:-1])
    n = __import__( module )
    for comp in parts[1:]:
        print(comp, n)
        print(dir(n))
        n = getattr(n, comp)          
    return n

LiveStrategies = {}