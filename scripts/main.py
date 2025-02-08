from pathlib import Path

folder_name = Path("store")

# Create folder if it does not exist
folder_name.mkdir(parents=True, exist_ok=True)

print(f"✅ Folder '{folder_name}' created successfully!")
