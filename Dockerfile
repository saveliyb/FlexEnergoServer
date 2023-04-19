FROM python:3.9.10
WORKDIR /code
#ENV PYTHONPATH = ${PYTHONPATH}:/app
COPY requirements.txt /code
COPY ./src /code
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]