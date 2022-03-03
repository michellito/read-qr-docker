FROM python:3

RUN apt-get update && apt-get install -y \
	python3-opencv ca-certificates python3-dev zbar-tools


RUN pip install torch==1.10.2 torchvision==0.11.3 -f https://download.pytorch.org/whl/cu111/torch_stable.html

RUN pip install 'git+https://github.com/facebookresearch/fvcore'
# install detectron2
RUN git clone https://github.com/facebookresearch/detectron2 detectron2_repo


RUN pip install -e detectron2_repo

# Set a fixed model cache directory.
ENV FVCORE_CACHE="/tmp"

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

ENV BINPATH /usr/bin
ADD read_qr.py $BINPATH
RUN chmod +x $BINPATH/read_qr.py

ENTRYPOINT [ "read_qr.py" ]