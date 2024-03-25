FROM python:3.11

COPY requirements.txt requirements.txt
RUN pip install -U pip setuptools wheel
RUN pip install -U spacy
RUN python -m spacy download en_core_web_sm
RUN pip install seaborn
RUN pip install --no-cache-dir -r requirements.txt

COPY . app
WORKDIR /app

EXPOSE 8000

ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]