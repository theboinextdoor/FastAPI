
#TODO: Use official Python image
FROM python:3.9-alpine

#TODO: Set working directory
WORKDIR /app

#TODO: Install FastAPI & Uvicorn
COPY requirements.txt .

#TODO: RUN pip install fastapi uvicorn
RUN pip install --no-cache-dir -r requirements.txt

#TODO: Copy app code into container
COPY . .

CMD ["uvicorn","main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]