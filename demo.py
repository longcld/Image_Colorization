# import the necessary packages
import os
import random
import argparse
import cv2 as cv
import keras.backend as K
import numpy as np
import sklearn.neighbors as nn

from config import img_rows, img_cols
from config import nb_neighbors, T, epsilon
from model import build_model

def parser_arg():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('--save', '-s', default="test", type=str, help="Folder to save test image prediction")
    parser.add_argument('--image', '-i', default=None, type=str, help="Path to test image")
    return parser.parse_args()

if __name__ == '__main__':
    arg = parser_arg()
    
    channel = 3
    
    model_weights_path = 'models/model.06-2.5489.hdf5'

    model = build_model()
    model.load_weights(model_weights_path)

#     print(model.summary())
    save_folder = arg.save
#     names_file = 'v_n.txt'

#     with open(names_file, 'r') as f:
#         names = f.read().splitlines()

#     samples = random.sample(names, 1)

#    samples = os.listdir(image_folder)

#     samples.append(image_name)
    h, w = img_rows // 4, img_cols // 4

    q_ab = np.load("data/pts_in_hull.npy")
    nb_q = q_ab.shape[0]

    nn_finder = nn.NearestNeighbors(n_neighbors=nb_neighbors, algorithm='ball_tree').fit(q_ab)

    filename = arg.image
    if len(arg.image.split('/')):
        image_name = arg.image.split('/')[-1]
    else:
        image_name = arg.image
#     filename = os.path.join(image_folder, image_name)
    print('Start processing image: {}'.format(filename))

    bgr = cv.imread(filename)
    gray = cv.imread(filename, 0)
    bgr = cv.resize(bgr, (img_rows, img_cols), cv.INTER_CUBIC)
    gray = cv.resize(gray, (img_rows, img_cols), cv.INTER_CUBIC)

    lab = cv.cvtColor(bgr, cv.COLOR_BGR2LAB)
    L = lab[:, :, 0]
    a = lab[:, :, 1]
    b = lab[:, :, 2]

    x_test = np.empty((1, img_rows, img_cols, 1), dtype=np.float32)
    x_test[0, :, :, 0] = gray / 255.

    X_colorized = model.predict(x_test)
    X_colorized = X_colorized.reshape((h * w, nb_q))

    X_colorized = np.exp(np.log(X_colorized + epsilon) / T)
    X_colorized = X_colorized / np.sum(X_colorized, 1)[:, np.newaxis]

    # Reweighted
    q_a = q_ab[:, 0].reshape((1, 313))
    q_b = q_ab[:, 1].reshape((1, 313))

    X_a = np.sum(X_colorized * q_a, 1).reshape((h, w))
    X_b = np.sum(X_colorized * q_b, 1).reshape((h, w))

    X_a = cv.resize(X_a, (img_rows, img_cols), cv.INTER_CUBIC)
    X_b = cv.resize(X_b, (img_rows, img_cols), cv.INTER_CUBIC)

    X_a = X_a + 128
    X_b = X_b + 128


    out_lab = np.zeros((img_rows, img_cols, 3), dtype=np.int32)
    out_lab[:, :, 0] = lab[:, :, 0]
    out_lab[:, :, 1] = X_a
    out_lab[:, :, 2] = X_b
    out_L = out_lab[:, :, 0]
    out_a = out_lab[:, :, 1]
    out_b = out_lab[:, :, 2]
    out_lab = out_lab.astype(np.uint8)
    out_bgr = cv.cvtColor(out_lab, cv.COLOR_LAB2BGR)
    out_bgr = out_bgr.astype(np.uint8)

    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    cv.imwrite(save_folder + '/{}_image.png'.format(image_name), gray)
   # cv.imwrite(save_folder + '/{}_gt.png'.format(image_name), bgr)
    cv.imwrite(save_folder + '/{}_out.png'.format(image_name), out_bgr)

    print("Done")

    K.clear_session()
