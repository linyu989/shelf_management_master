# 仓库动画仿真

## 功能说明

    生成一定行列的货架并完成一段时间内以特定方法出入库的动画演示和保存

## 运行方式

    1.安装requirements.txt里面所有包
    2.运行main.py文件(可根据参数说明修改对应参数)

## 项目结构

    shelf_management_master
    │  main.py  //主函数
    │  README.md
    │       
    ├─data      //资源文件夹
    ├─output    //图片输出文件夹
    │      
    ├─simulation
    │  │  storage_map.py    //地图生成与更新
    │          
    ├─sim_ani
    │      animation.py     //动画渲染
    │      
    ├─sim_control
    │      shelf_alter.py   //仓库出入库控制
    │      
    └─test
            mytest.py       //测试

## 参数说明

    仓库参数
    cell_size = [150, 150]  #货架单元大小,格子高和宽
    cells_shape = [24, 12]  #货架行数和列数
    
    # 总运行时间,入库起始时间,出库起始时间,出入库周期
    # 出入库周期一致保证能一直有货物可出库
    total_time, start_in, start_out, period = 1400, 5, 200, 7
    
    # 选择入库方法
    flag = 2  # flag=0,1,2 依次为单个顺序进出库，单个随机入库顺序出库,4个单元随机入库顺序出库
    
    # 单个货架随机入库时摆放所用货架列数
    random_length = 12
    # 4个货架随机入库摆放所用货架列数,不能超过货架最大列数
    mult_random_length = 12
    
    # 是否保存gif图片
    gif_save = 0  # 0表示不保存,1表示保存，默认不保存