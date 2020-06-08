FROM python:3
COPY release_data.json .
COPY release_main.py .
COPY requirements.txt .
WORKDIR .
RUN pip install -r requirements.txt
RUN python3 -m pip install z3-solver

CMD ["python","release_main.py"]