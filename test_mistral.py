import mistralai
print(f"mistralai path: {mistralai.__path__}")
import pkgutil
print("Submodules:")
for loader, module_name, is_pkg in pkgutil.walk_packages(mistralai.__path__):
    print(f"- {module_name}")

