import time
import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv
import google.generativeai as genai

folder_to_track = "C:/Users/zoraw/Downloads"

extensions_map = {
    '.jpg': 'Images',
    '.png': 'Images',
    '.jpeg': 'Images',
    '.pdf': 'Documents',
    '.docx': 'Documents',
    '.txt': 'Documents',
    '.zip': 'Compressed',
    '.exe': 'Installers',
    '.dmg': 'Installers',
    '.msi': 'Installers',
    '.mp4': 'Videos'
}

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")


if not api_key:
    print("Error! API Key not found.")
    exit()
else:
    genai.configure(api_key = api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

def get_ai_folder(filename):
    
    if not api_key:
        return "Unclassified"
    while True:
        try:
            response = model.generate_content(f"I have a file named '{filename}'. Classify it into one of these folders: [Finance, School, Personal, Work, Installers]. Return ONLY the folder name.")

            return response.text.strip()
        except exceptions.ResourceExhausted:
            print("Limit exceeded. Retrying in 20 seconds...")
            time.sleep(20)
            
        except Exception as e:
            print(f"Unexpected error on {filename}: {e}")
            return "Unclassified"

    


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        
        for file in os.listdir(folder_to_track):
            
            if file.endswith('.crdownload') or file.endswith('.part') or file.startswith('.'):
                continue
            
            src = f"{folder_to_track}/{file}"
            
            if os.path.isdir(src):
                continue
            
            if os.path.isfile(src):
                _, ext = os.path.splitext(file)
                ext = ext.lower()
                
                if ext in extensions_map:
                    folder = extensions_map[ext]
                else:
                    print(f"Unknown extension for {file}, Asking AI....")
                    folder = get_ai_folder(file)
                
                destination_folder = f"{folder_to_track}/{folder}" 
                
                
                if not os.path.exists(destination_folder):
                    os.makedirs(destination_folder)
                
                file_path = f"{destination_folder}/{file}"
                
                if not os.path.exists(file_path):
                    try:
                        shutil.move(src, file_path)
                        print(f"Moved {file} -> {destination_folder}")
                    except Exception as e:
                        print(f"Error moving {file}: {e}")
                
            
            # print(f"I see a file: {file}")
    
    
if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_to_track, recursive = True)
    
    print(f"Monitoring Folder: {folder_to_track}")
    print("Press Ctrl+C to stop")
    
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()
    
    