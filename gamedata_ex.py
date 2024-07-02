import os
from UnityPy import AssetsManager

def extract_json(bundle_path, output_dir):
    # Создаем экземпляр AssetsManager
    am = AssetsManager(bundle_path)

    # Перебираем все объекты в пакете
    for asset in am.assets:
        for obj in asset.objects.values():
            # Извлекаем данные
            data = obj.read()

            # Проверяем, является ли объект файлом CombinedGameData.json
            if 'CombinedGameData.json' in str(data):
                # Извлекаем json
                json_data = data.text

                # Записываем json в файл
                with open(os.path.join(output_dir, 'CombinedGameData.json'), 'w') as f:
                    f.write(json_data)

# Основная директория
main_dir = r'C:\Users\houne\Downloads\Telegram Desktop\1'

# Директория для сохранения извлеченных файлов
save_dir = os.path.join(os.getcwd(), 'gamedata')

# Обходим все поддиректории
for subdir in os.listdir(main_dir):
    subdir_path = os.path.join(main_dir, subdir)
    
    # Проверяем, является ли это директорией
    if os.path.isdir(subdir_path):
        # Путь к файлу gamedata_bundle
        bundle_path = os.path.join(subdir_path, 'gamedata_bundle')
        
        # Путь для сохранения извлеченного файла
        output_dir = os.path.join(save_dir, subdir)
        
        # Создаем директорию, если она еще не существует
        os.makedirs(output_dir, exist_ok=True)
        
        # Вызываем функцию
        extract_json(bundle_path, output_dir)
