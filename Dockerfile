FROM python:3.11

COPY app/requirements.txt app/requirements.txt
RUN pip install -U pip setuptools wheel
RUN pip install -U spacy
RUN python -m spacy download en_core_web_sm
RUN pip install seaborn
RUN pip install --no-cache-dir -r app/requirements.txt

COPY . app
WORKDIR /app

EXPOSE 8000

ENTRYPOINT ["python", "app/manage.py"]
CMD ["runserver", "0.0.0.0:8000"]