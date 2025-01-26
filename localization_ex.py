import UnityPy
import os

# Path to the bundle and output directory
bundle_path = "input/translations_bundle"
output_dir = "localization"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Load the bundle
env = UnityPy.load(bundle_path)

# Iterate through all objects in the bundle
for obj in env.objects:
    # Check if the object is a TextAsset
    if obj.type.name == "TextAsset":
        data = obj.read()
        # Check if the object's name attribute exists and ends with .ini
        if hasattr(data, 'm_Name') and data.m_Name.endswith(".ini"):
            # Define the output path
            output_path = os.path.join(output_dir, data.m_Name)
            # Write the content to a file with encoding
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(data.m_Script)
            print(f"File {data.m_Name} has been extracted and saved to {output_path}")
