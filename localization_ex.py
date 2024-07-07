import UnityPy
import os

# Путь к бандлу и выходной папке
bundle_path = "input/translations_bundle"
output_dir = "localization"

# Убедитесь, что выходная папка существует
os.makedirs(output_dir, exist_ok=True)

# Загружаем бандл
env = UnityPy.load(bundle_path)

# Проходим через все объекты в бандле
for obj in env.objects:
    # Проверяем, является ли объект текстовым файлом (TextAsset)
    if obj.type.name == "TextAsset":
        data = obj.read()
        # Проверяем, заканчивается ли имя файла на .ini
        if data.name.endswith(".ini"):
            # Путь для сохранения файла
            output_path = os.path.join(output_dir, data.name)
            # Записываем содержимое в файл
            with open(output_path, 'wb') as f:
                f.write(data.script)
            print(f"Файл {data.name} был извлечён и сохранён в {output_path}")
