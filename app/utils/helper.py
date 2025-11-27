from fastapi import UploadFile, File, Form
import uuid
import os
import shutil

BASE_UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")
def uploadFile(file: UploadFile, destination_folder: str) -> dict:
    try: 
        if file is not None:
            file.file.seek(0)
            
            file_extension = os.path.splitext(file.filename)[1]
            filename = f"{uuid.uuid4().hex}{file_extension}"
            
            upload_dir = os.path.join(BASE_UPLOAD_DIR, destination_folder)
            os.makedirs(upload_dir, exist_ok=True)

            file_location = os.path.join(upload_dir, filename)

            with open(file_location, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            return {
                'data': filename,
                'message': 'File uploaded successfully',
                'status': True,
            }
    except Exception as e:
        return {
            'data': None,
            'message': f'File upload failed: {str(e)}',
            'status': False,
        }
        
    return {
        'data': None,
        'message': 'No file provided',
        'status': False,
    }