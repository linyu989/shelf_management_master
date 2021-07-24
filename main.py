"""
 @Author       :linyu
 @File         :main.py
 @Description  :主函数
 @Software     :PyCharm
"""

import numpy as np
import matplotlib.pyplot as plt
import random
import time
import copy

from simulation import storage_map
from sim_ani import animation
from sim_control import shelf_alter

plt.rcParams['figure.dpi'] = 300

'''
主函数
'''


def show_main():
    pass


if __name__ == '__main__':
    start_time = time.time()

    # 尺寸参数
    # map_size = [3840, 2160]
    cell_size = [150, 150]
    cells_shape = [24, 12]
    # 仓库尺寸由货架参数计算可得
    map_h = int((cells_shape[0] + 2) * cell_size[0])
    map_w = int((cells_shape[1] + 2) * cell_size[1])
    map_size = [map_h, map_w]
    # 入库参数
    total_time, start_in, start_out, period = 1400, 5, 100, 7
    # 入库方法
    flag = 2  # flag=0,1,2 依次为单个顺序进出库,单个随机入库顺序出库,4个单元随机入库顺序出库
    # 是否保存gif图片
    gif_save = 0  # 0表示不保存,1表示保存,默认不保存

    # 单个货架随机入库的长度
    random_length = 23
    # 4个货架随机入库的长度,不能超过货架列数
    mult_random_length = 12
    mult_random_length = mult_random_length if mult_random_length <= cells_shape[1] else cells_shape[1]

    '''
    类方法调用得到alternate_dict_list
    '''
    # map类实例化
    originmap = storage_map.originMap(map_size, cell_size, cells_shape)
    origin_map_img, alternate_dict_list = originmap.origin_map()
    alternate_dict_list_init = copy.deepcopy(alternate_dict_list)

    '''
    进行动画制作
    '''
    # ani与control类完成动画与进出库
    ani = animation.simAnimation(alternate_dict_list_init, map_size, cell_size, cells_shape)
    alter_shelf = shelf_alter.alterShelf(alternate_dict_list, cells_shape, total_time, start_in, start_out, period)

    # alter_map绘制地图
    alter_map = storage_map.alternateMap(map_size, alternate_dict_list, cells_shape)
    img = alter_map.alternate_map(map_size, alternate_dict_list, cells_shape)

    # alter_shelf方法测试
    if flag == 0:
        mult_random_update_cells = alter_shelf.unit_sequence()
        end_time = time.time()
        print(f"用时:{end_time - start_time}")
        ani.show_simu(mult_random_update_cells, gif_save=gif_save)

    elif flag == 1:
        mult_random_update_cells = alter_shelf.unit_random_in(random_length)
        end_time = time.time()
        print(f"用时:{end_time - start_time}")
        ani.show_simu(mult_random_update_cells, gif_save=gif_save)

    elif flag == 2:
        mult_random_update_cells = alter_shelf.mult_random_in(mult_random_length)
        end_time = time.time()
        print(f"用时:{end_time - start_time}")
        ani.show_simu(mult_random_update_cells, gif_save=gif_save)
    else:
        print("[INFO] Error Flag!!!")
