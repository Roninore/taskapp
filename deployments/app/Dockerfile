FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt && rm requirements.txt

COPY /taskapp /app/taskapp

CMD ["python", "-m", "taskapp.app"]
