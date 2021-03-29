FROM python:3

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ENV BINPATH /usr/bin
ADD transfer.py $BINPATH
RUN chmod +x $BINPATH/transfer.py

ENTRYPOINT [ "python", "transfer.py" ]