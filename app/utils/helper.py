from fastapi import UploadFile, File, Form
import uuid
import os
import shutil

def uploadFile(file: UploadFile, destination_folder: str) -> str:
    """
    Save an UploadFile to the specified destination folder and return the file path.
    """
    try: 
        if file is not None:
            # reset pointer ของไฟล์ก่อนเขียน
            file.file.seek(0)
            
            file_extension = os.path.splitext(file.filename)[1]
            filename = f"{uuid.uuid4().hex}{file_extension}"
            
            upload_dir = "uploads/" + destination_folder
            os.makedirs(upload_dir, exist_ok=True)

            file_location = f"{upload_dir}/{filename}"

            with open(file_location, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            return {
                'data': file_location,
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