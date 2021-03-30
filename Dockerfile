FROM python:3

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

ENV BINPATH /usr/bin
ADD transfer.py $BINPATH
RUN chmod +x $BINPATH/transfer.py

ENTRYPOINT [ "transfer.py" ]