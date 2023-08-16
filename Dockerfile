FROM python:3.10-alpine
COPY requirements.txt /
RUN pip install -r requirements.txt && rm requirements.txt
COPY ./src /home/app/
WORKDIR /home/app/
CMD ["uvicorn", "main:app", "--reload", "--host=0.0.0.0"]
