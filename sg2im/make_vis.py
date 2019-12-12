import numpy as np
import cv2
import os

images = ['img000022.png', 'img000030.png', 'img000035.png', 'img000043.png', 'img000049.png', 'img000094.png']
scene_graphs = ['sg000022.png', 'sg000030.png', 'sg000035.png', 'sg000043.png', 'sg000049.png', 'sg000094.png']

img_dir = 'grid_imgs'
outfile = 'grid.png'

imgs = [cv2.imread(os.path.join(img_dir, img)) for img in images]
sgs = [cv2.imread(os.path.join(img_dir, sg)) for sg in scene_graphs]

print("====number of images====")
print(len(images))
print(len(scene_graphs))

imgs = imgs + sgs
print("====concat list====")
print(len(imgs))

if any(i.shape != imgs[0].shape for i in imgs[1:]):
    raise ValueError("Not all images have the same shape")

img_h, img_w, img_c = imgs[0].shape

m_x = 0
m_y = 0
# if args.margin is not None:
#     margin = args.margin[0]
#     if '.' in margin:
#         m = float(margin)
#         m_x = int(m*img_w)
#         m_y = int(m*img_h)
#     else:
#         m_x = int(margin)
#         m_y = m_x

imgmatrix = np.zeros((img_h * h + m_y * (h - 1),
                      img_w * w + m_x * (w - 1),
                      img_c),
                     np.uint8)

imgmatrix.fill(255)

positions = itertools.product(range(w), range(h))
for (x_i, y_i), img in itertools.izip(positions, imgs):
    x = x_i * (img_w + m_x)
    y = y_i * (img_h + m_y)
    imgmatrix[y:y+img_h, x:x+img_w, :] = img

cv2.imwrite(outfile, imgmatrix)


