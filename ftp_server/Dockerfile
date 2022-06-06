FROM python:3.9

COPY *.py /app/
WORKDIR /app

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

CMD echo "No command defined!.."
