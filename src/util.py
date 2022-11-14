import numpy as np
import open3d as o3d
from PIL import Image, ImageFont, ImageDraw
from pyquaternion import Quaternion

def text_3d(text, pos, direction=None, degree=0.0, density=10, font='/usr/share/fonts/truetype/freefont/FreeMono.ttf', font_size=10):
        """
            Create a 3D text object in o3d visualizer.

            :param text: text to be displayed
            :param pos: position of the text
            :param direction: direction of the text
            :param degree: rotation of the text
            :param density: density of the text
            :param font: font of the text
            :param font_size: font size of the text

            :return: o3d.geometry.PointCloud object
        """

        font_obj = ImageFont.truetype(font, font_size * density)
        font_dim = font_obj.getsize(text)

        img = Image.new('RGB', font_dim, color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), text, font=font_obj, fill=(0, 0, 0))
        img = np.asarray(img)
        img_mask = img[:, :, 0] < 128
        indices = np.indices([*img.shape[0:2], 1])[:, img_mask, 0].reshape(3, -1).T

        pcd = o3d.geometry.PointCloud()
        pcd.colors = o3d.utility.Vector3dVector(img[img_mask, :].astype(float) / 255.0)
        pcd.points = o3d.utility.Vector3dVector(indices / 1000 / density)

        pcd.translate(pos)

        return pcd