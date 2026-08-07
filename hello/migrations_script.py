import os
import shutil

def clean_migrations():
    # 1. Purani db.sqlite3 file ko delete karna
    db_path = os.path.join(os.getcwd(), 'db.sqlite3')
    if os.path.exists(db_path):
        os.remove(db_path)
        print("✅ Puraani 'db.sqlite3' file delete ho gayi.")

    # 2. Har app ki migration files ko delete karna
    base_dir = os.getcwd()
    for root, dirs, files in os.walk(base_dir):
        # Hum sirf '.venv' ya 'node_modules' ko skip kar rahe hain taaki speed bani rahe
        if '.venv' in root or 'node_modules' in root:
            continue
            
        if os.path.basename(root) == 'migrations':
            print(f"\n📂 Cleaning: {root}")
            for file in files:
                if file != '__init__.py' and file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                    print(f"   ❌ Deleted migration file: {file}")
                    
            # Agar '__pycache__' folder hai migrations ke andar, toh use bhi uda do
            pycache_path = os.path.join(root, '__pycache__')
            if os.path.exists(pycache_path):
                shutil.rmtree(pycache_path)
                print("   ❌ Deleted __pycache__ folder")

    print("\n🚀 Saari migrations saaf ho gayi hain! Ab aap fresh commands chala sakte hain.")

if __name__ == '__main__':
    clean_migrations()
