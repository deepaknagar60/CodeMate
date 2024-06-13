import os
from fastapi import APIRouter, UploadFile, File, Form
from ...utils.answer import run
import zipfile
from fastapi.responses import JSONResponse
from fastapi import HTTPException
import shutil

router = APIRouter()




@router.post("/upload")
async def upload_file( prompt: str = Form(...), file: UploadFile = File(...)):
    try:
        os.makedirs('uploads', exist_ok=True)

        zip_file_path = os.path.join('uploads', file.filename)
        with open(zip_file_path, 'wb+') as destination:
            file_content = await file.read()
            destination.write(file_content)

        # Extract the zip file
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall('uploads')
        
        os.remove(zip_file_path)
        
        documentation = {}
        
        filename = zip_file_path.replace('.zip', '')
        
        extracted_files = os.listdir(filename)
        for extracted_file in extracted_files:
            file_path = os.path.join(filename, extracted_file)
            
            answer = run(file_path,prompt)
            print(answer)
            documentation[extracted_file] = answer
            
            os.remove(file_path)

        
        shutil.rmtree(filename)

        return JSONResponse(status_code=200, content=documentation)

    except Exception as e:
        
        return JSONResponse(status_code=500, error='Error occured while processing files..')
