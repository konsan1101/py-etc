import chainer
from chainercv.links import SSD300
from chainercv import utils
from chainercv.datasets import voc_bbox_label_names


def item_detection(img_file):
    """
    Recieve a image file for detection.
    Return detected data  to create 'Item' model
    :param img_file:
    :return:  bbox, name, score
    """

    chainer.config.train = False

    # Define the detection model
    model = SSD300(
        n_fg_class=len(voc_bbox_label_names),
        pretrained_model='voc0712')

    img = utils.read_image(img_file, color=True)
    bboxes, labels, scores = model.predict([img])
    bbox, name, score = bboxes[0], labels[0], scores[0]

    return name, score
