#!/usr/bin/env python

import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()

# import some common libraries
import numpy as np
import os, json, cv2, random

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer, ColorMode
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.data.datasets import register_coco_instances

import requests
import argparse

from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol


print('here')

parser = argparse.ArgumentParser(
    description='Transfer ReadsPerGene.out.tab files generated by STAR to DMAC Olympus server.'
)

parser.add_argument('--file',
                       type=str,
                       help='input photo')

parser.add_argument('--type',
                       type=str,
                       help='root or leaf')

parser.add_argument('--model',
                       type=str,
                       help='model file')



args = parser.parse_args()
print(args)

cfg = get_cfg()
cfg.MODEL.DEVICE='cpu'
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg.DATASETS.TEST = ()
cfg.DATALOADER.NUM_WORKERS = 2
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")  # Let training initialize from model zoo
cfg.SOLVER.IMS_PER_BATCH = 2
cfg.SOLVER.BASE_LR = 0.00025  # pick a good LR
cfg.SOLVER.MAX_ITER = 1000    # 300 iterations seems good enough for this toy dataset; you will need to train longer for a practical dataset
cfg.SOLVER.STEPS = []        # do not decay learning rate
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1  # only has one class (qrcode). (see https://detectron2.readthedocs.io/tutorials/datasets.html#update-the-config-for-new-datasets)
cfg.MODEL.WEIGHTS = args.model  # path to the model we just trained
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7   # set a custom testing threshold

os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
predictor = DefaultPredictor(cfg)

# test image
im = cv2.imread(args.file)
outputs = predictor(im)  # format is documented at https://detectron2.readthedocs.io/tutorials/models.html#model-output-format

pred_boxes = outputs["instances"].pred_boxes

for bbox in pred_boxes:
  print(bbox)

  # (x0, y0, x1, y1)

  x0 = round(bbox[0].item())
  y0 = round(bbox[1].item())
  x1 = round(bbox[2].item())
  y1 = round(bbox[3].item())

  crop_img = im[ y0:y1, x0:x1]

  # zbar
  results = decode(crop_img, symbols=[ZBarSymbol.QRCODE])
  print(results)

# data = {
#     'rename': args.rename,
#     'path': args.path,
#     'token': args.token
# }


# response = requests.post('https://demeter.pharmacy.arizona.edu/api/file-transfer/', files=file_dict, data=data)
# print(str(response.text))