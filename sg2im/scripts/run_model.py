#!/usr/bin/python
#
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse, json, os

from imageio import imwrite
import torch

from sg2im.model import Sg2ImModel
from sg2im.data.utils import imagenet_deprocess_batch
import sg2im.vis as vis


parser = argparse.ArgumentParser()
parser.add_argument('--checkpoint', default='sg2im-models/vg128.pt')
parser.add_argument('--scene_graph_dir', default='scene_graphs/')
parser.add_argument('--output_dir', default='outputs')
parser.add_argument('--draw_scene_graphs', type=int, default=1)
parser.add_argument('--device', default='gpu', choices=['cpu', 'gpu'])


def main(args):
  if not os.path.isfile(args.checkpoint):
    print('ERROR: Checkpoint file "%s" not found' % args.checkpoint)
    print('Maybe you forgot to download pretraind models? Try running:')
    print('bash scripts/download_models.sh')
    return

  if not os.path.isdir(args.output_dir):
    print('Output directory "%s" does not exist; creating it' % args.output_dir)
    os.makedirs(args.output_dir)

  if args.device == 'cpu':
    device = torch.device('cpu')
  elif args.device == 'gpu':
    device = torch.device('cuda:0')
    if not torch.cuda.is_available():
      print('WARNING: CUDA not available; falling back to CPU')
      device = torch.device('cpu')

  # Load the model, with a bit of care in case there are no GPUs
  map_location = 'cpu' if device == torch.device('cpu') else None
  checkpoint = torch.load(args.checkpoint, map_location=map_location)
  model = Sg2ImModel(**checkpoint['model_kwargs'])
  model.load_state_dict(checkpoint['model_state'])
  model.eval()
  model.to(device)

  SCENE_GRAPH_DIR = args.scene_graph_dir

  scene_graphs = []
  # Load the scene graphs
  for filename in os.listdir(SCENE_GRAPH_DIR):
    print("opening file: {}".format(filename))
    with open(os.path.join(SCENE_GRAPH_DIR, filename), 'r') as f:
      sg = json.load(f)
      scene_graphs.append(sg)

  for sg_idx, sg in enumerate(scene_graphs):
    # Run the model forward
    with torch.no_grad():
      try:
        imgs, boxes_pred, masks_pred, _ = model.forward_json(sg)
      except ValueError as err:
        print("ValueError: {}".format(err))
        continue
    imgs = imagenet_deprocess_batch(imgs)

    # Save the generated images
    for i in range(imgs.shape[0]):
      img_np = imgs[i].numpy().transpose(1, 2, 0)
      img_path = os.path.join(args.output_dir, 'img%06d.png' % sg_idx)
      imwrite(img_path, img_np)

    # Draw the scene graphs
    if args.draw_scene_graphs == 1:
      for i, sg_ in enumerate(sg):
        sg_img = vis.draw_scene_graph(sg_['objects'], sg_['relationships'])
        sg_img_path = os.path.join(args.output_dir, 'sg%06d.png' % sg_idx)
        imwrite(sg_img_path, sg_img)


if __name__ == '__main__':
  args = parser.parse_args()
  main(args)

