CUDA_VISIBLE_DEVICES=0 python scripts/run_model.py \
  --checkpoint sg2im-models/vg128.pt \
  --scene_graph_dir /vision/u/kevintan/sg2im/grid_imgs_scene_graphs \
  --output_dir grid_imgs_results \
  --device gpu