"""
 @Author       :linyu
 @File         :storage_map.py
 @Description  :仓库地图生成与更新
 @Software     :PyCharm
"""
import numpy as np
import matplotlib.pyplot as plt
import random

plt.rcParams['figure.dpi'] = 500  # 分辨率

'''
根据仓库和货架单元尺寸生成仓库地图
'''


class originMap():
    def __init__(self, map_size, cell_size, cells_shape):
        self.map_size = map_size
        self.cell_size = cell_size
        self.cells_shape = cells_shape

    # 货架单元渲染
    def render(self, img, corner, size, color):
        # cell坐标点
        start_h, start_w = corner[0], corner[1]
        # size宽高
        size_h, size_w = size[0], size[1]
        # size长宽调节边界避免格子相连
        dh = int(size[0] / 10)
        dw = int(size[1] / 10)

        img[(start_h + dh):(start_h + size_h), (start_w + dw):(start_w + size_w)] = color

        return img

    # 原始地图
    def origin_map(self):
        red = np.zeros(self.map_size, dtype=np.uint8)
        green = np.zeros(self.map_size, dtype=np.uint8)
        blue = np.zeros(self.map_size, dtype=np.uint8)
        red[:, :] = 255
        green[:, :] = 255
        blue[:, :] = 255
        img = np.dstack((red, green, blue))

        shelf_unload_color = [204, 255, 204]
        shelf_load_color = [255, 102, 0]

        cell_size = self.cell_size
        edge_h, edge_w = cell_size[0], cell_size[1]
        cell_coord_h, cell_coord_w = edge_h, edge_w
        corner = None
        dict_list = {}
        flag = 0

        for i in range(self.cells_shape[0]):
            for j in range(self.cells_shape[1]):
                index = [i, j]
                corner = [cell_coord_h, cell_coord_w]
                # 生成{index:[[corner,cell_size,flag=0],}的字典
                dict_list[str(index)] = [corner, cell_size, flag]
                self.render(img, corner, cell_size, shelf_unload_color)
                cell_coord_w += cell_size[1]
            cell_coord_w = edge_w
            cell_coord_h += cell_size[0]

        # print(dict_list)
        return img, dict_list


'''
alternateMap由字典生成与更新图像
'''


class alternateMap():
    def __init__(self, map_size, alternate_cells_dict, cells_shape):
        self.map_size = map_size
        self.alternate_cells_dict = alternate_cells_dict
        self.cells_shape = cells_shape

    def alternate_cells_render(self, img, corner, cell_size, flag):
        color = [204, 255, 204] if flag == 0 else [255, 102, 0]
        start_h, start_w = corner[0], corner[1]
        size_h, size_w = cell_size[0], cell_size[1]
        dh = int(cell_size[0] / 5)
        dw = int(cell_size[1] / 5)

        img[int(start_h + dh):(start_h + size_h), int(start_w + dw):(start_w + size_w)] = color

        return img

    def alternate_map(self, map_size, alternate_cells_dict, cells_shape):
        red = np.zeros(map_size, dtype=np.uint8)
        green = np.zeros(map_size, dtype=np.uint8)
        blue = np.zeros(map_size, dtype=np.uint8)
        red[:, :] = 255
        green[:, :] = 255
        blue[:, :] = 255
        img = np.dstack((red, green, blue))

        edge_h, edge_w = 0, 0

        for i in range(cells_shape[0]):
            for j in range(cells_shape[1]):
                index = [i, j]
                corner = alternate_cells_dict[str(index)][0]
                corner = [corner[0] + edge_h, corner[1] + edge_w]
                cell_size = alternate_cells_dict[str(index)][1]
                flag = alternate_cells_dict[str(index)][2]
                self.alternate_cells_render(img, corner, cell_size, flag)

        return img

    def update_alternate_map(self, map_size, update_cells, cells_shape):
        alternate_cells_dict = self.alternate_cells_dict
        new_cells_dict = alternate_cells_dict

        for cell in update_cells:
            [index, flag] = cell
            new_cells_dict[str(index)][-1] = flag

        img = self.alternate_map(map_size, new_cells_dict, cells_shape)

        return img

    def update_unit_alternate_map(self, map_size, update_cell, cells_shape):
        alternate_cells_dict = self.alternate_cells_dict
        new_cells_dict = alternate_cells_dict
        [index, flag] = update_cell
        # 对原始dict进行更新
        new_cells_dict[str(index)][-1] = flag
        img = self.alternate_map(map_size, new_cells_dict, cells_shape)

        return img


def plt_show(img):
    print("imgreal================================")
    print(img.shape, img.dtype)

    plt.imshow(img)
    # plt.axis('off')

    # 保存图片
    # plt.savefig(f'./output/origin_map_{str(random.randint(0,9999))}.png', dpi=700)

    plt.show()


if __name__ == '__main__':
    map_h, map_w = 3840, 2160
    map_size = [map_h, map_w]
    cell_size = [150, 150]
    cells_shape = [24, 12]

    # 字典直接内部打印不用返回，该函数还需要外部调用只需要img
    # img, dict_list = origin_map(map_size, cell_size, cell_num)
    # img = origin_map(map_size, cell_size, cells_shape)

    # print(dict_list)

    originmap = originMap(map_size, cell_size, cells_shape)

    origin_map_img, alternate_dict_list = originmap.origin_map()

    alter_map = alternateMap(map_size, alternate_dict_list, cells_shape)

    img = alter_map.alternate_map(map_size, alternate_dict_list, cells_shape)

    # 更新地图
    update_cells = []
    flag = 1
    for num in range(random.randint(min(cells_shape), cells_shape[0] * cells_shape[1])):
        index = [np.random.randint(0, cells_shape[0]), np.random.randint(0, cells_shape[1])]
        update_cells.append([index, flag])

    print(update_cells)

    img = alter_map.update_alternate_map(map_size, update_cells, cells_shape)

    # img =alter_map.update_alternate_map(map_size, [[[22, 1], 1]], cells_shape)

    # img = alter_map.update_unit_alternate_map(map_size,[[22, 1], 1],cells_shape)

    plt_show(img)
