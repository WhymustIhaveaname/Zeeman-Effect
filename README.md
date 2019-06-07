# Zeeman-Effect
##数据分析
* 我们发现使用取三点做圆的方法误差很大, 其原因有:
    1. 图像上其实不是一个完美的圆, 而是一个很接近圆的椭圆
    2. 只用三个点不能完全利用图像上的信息----不能完全利用信息也就意味着误差的增大
    
    于是我们决定亲自编写程式进行误差分析, 原计划让计算机自动识别圆并且拟合, 但是效果不好, 原因是计算机在低对比度的图像边缘的表现很差, 而图像边缘的点对于拟合数据来说是很关键的(边缘的点的 condition number 是中间的点的好几倍), 所以最后决定采用人工标记+取很多点最小二乘的策略. 我们编写了程式如 https://github.com/WhymustIhaveaname/Zeeman-Effect/anaData.py, 其有如下的优点:
    1. 具有GUI
    2. 使用椭圆进行拟合, 拟合效果更好
    3. 可以点很多冗余的点进行最小二乘
    4. 可以给出拟合的误差
    5. 在点点的同时实时显示拟合结果, 便于立即发现 fake minium 和 直观感受不同区域的点的 condition number
    6. 在左键取点后支持使用键盘上的 wasd 进行以1像素为单位的微调；并且支持使用 backspace 依次删除点.
    7. 支持使用键盘上的 c 改变颜色使点和圆更清晰
    
    下图展示了我们的程式的工作情况, 下下图示例了如果使用圆来拟合会怎样, 说明了使用椭圆拟合的必要性. 这两张图片中, 为了使点和圆更明显, 我加粗了线条, 实际工作中使用了更细的线条以达到更高的精度.
    
    [程式的界面](https://github.com/WhymustIhaveaname/Zeeman-Effect/fitwitheclipse.png)
    [使用圆拟合](https://github.com/WhymustIhaveaname/Zeeman-Effect/fitwithcircle.png)
