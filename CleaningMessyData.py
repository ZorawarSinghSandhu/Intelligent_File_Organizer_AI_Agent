data_stream = [
    {"id": 101, "filename": "report.pdf", "size_mb": 5, "status": "valid"},
    {"id": 102, "filename": "image.png", "size_mb": 12, "status": "valid"},
    {"id": 103, "filename": "virus.exe", "size_mb": 200, "status": "malware"},
    {"id": 104, "filename": "notes.txt", "size_mb": "ERROR", "status": "valid"}, # Dirty data!
    {"id": 105, "filename": "backup.zip", "size_mb": 50, "status": "valid"}
]

total_size = 0
for data in data_stream:
    if data["status"] == "valid":
        try:
            total_size += data["size_mb"]
        except TypeError:
            print(f"Corrupt data found in file: [{data["filename"]}]")

print(f"Total valid size: {total_size} MB")