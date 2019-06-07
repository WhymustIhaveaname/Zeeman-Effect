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
    
    ![image](./fitwitheclipse.png)
    ![image](./fitwithcircle.png)

* 对红光, 磁场平行于光路的情况进行处理, 得到原始数据如下表所示. 其中 C1--C6 是从内到外的六个圆, $r^2$ 单位为像素的平方, $\sigma$ 为 $r^2$ 的误差. 半径使用的是长短轴的平均值, 因为我们知道, 任何的缩放比例都会被之后的数据处理消去, 所以平均长短轴以减小误差.
    
    ##### 红光, 磁场平行于光路
    |x(mm)|B(mT)|C1||C2||C3||C4||C5||C6||
    |-----|-----|-|-|-|-|-|-|-|-|-|-|-|-|
    |||$r^2$|$\sigma$|$r^2$|$\sigma$|$r^2$|$\sigma$|$r^2$|$\sigma$|$r^2$|$\sigma$|$r^2$|$\sigma$|$r^2$|
    |41.0|547.28|21838|0.79|29241|0.48|37272|1.24|55960|0.72|64273|0.31|72017|0.80|
    |41.5|519.15|21295|0.44|28433|0.39|36149|0.74|55531|0.98|63781|0.56|71310|0.76|
    |42.0|492.77|21374|0.76|28258|0.72|35306|0.61|55932|1.02|62901|0.18|70543|0.65|
    |42.5|468.02|22141|0.41|28291|0.38|34820|1.31|56216|0.72|63353|0.75|71610|0.67|
    |43.0|444.78|21934|0.27|28291|0.66|34820|0.62|55790|1.26|63303|0.96|69222|0.46|
    |43.5|422.95|22183|0.54|28322|0.84|34373|0.84|56745|0.99|62804|0.38|69183|0.32|
    |44.0|402.42|22275|0.35|28408|0.79|34015|0.46|57055|0.44|63058|0.29|69072|0.60|
    |44.5|383.10|22676|0.33|27833|0.23|33521|0.60|56952|0.56|63091|0.70|68489|0.54|
    |45.0|364.91|22728|0.19|27998|0.23|33258|0.25|56567|0.49|62747|0.40|68839|0.44|
    
* 接下来的数据处理有两种方法, 其一是利用

    $\Delta k=\frac{1}{2\mu t}(\frac{r_{p+1,a}^2}{r_{p+1,a}^2-r_{p,a}^2}-\frac{r_{p+1,b}^2}{r_{p+1,b}^2-r_{p,b}^2})$
    
    而另一种方法是利用
    
    $\Delta k=\frac{1}{2\mu t}\frac{\delta}{\Delta}$
    
    这两种方法处理得到的结果理论上是一致的, 但实际上后者误差更小. 其原因是, 由原始数据便可以看出, 本实验的误差还是很大的, 并且公式中还涉及到减法, 这会进一步加大误差, 而第二种方法利用 $r_{p+1,a}^2-r_{p,a}^2$ 的特性减小了 $\Delta$ 的误差, 误差也就小一些了. 意识到这一点后, 我们进一步改进误差处理的方法, 首先由
    
    $\Delta=average(r_{4}^2-r_{1}^2,r_{5}^2-r_{2}^2,r_{6}^2-r_{3}^2)$
    
    计算出 $\Delta$, 再由 $\delta_i=r_{i+4}^2-r_{i+3}^2$ 计算出 $\delta_1$, $\delta_2$, 之后再用 $\Delta k=\frac{1}{2\mu t}\frac{\delta}{\Delta}$ 得到波数差. 处理后的数据如下表所示. 每一个 $\sigma$ 都代表了它前面的量的误差, 单位为 percent. 其他量默认单位为像素的平方.
    
    ##### 红光, 磁场平行于光路
    |x(mm)|$\Delta$|$\sigma$|$\delta_1$|$\delta_1 \over \Delta$|$\sigma$|$\delta_2$|$\delta_2 \over \Delta$|$\sigma$|
    |-----|--------|--------|----------|-----------------------|--------|----------|-----------------------|--------|
    |41.0|31300|1.1|8313|0.2656|5.5|7744|0.2474|8.0|
    |41.5|34915|1.0|8250|0.2376|7.9|7529|0.2169|8.7|
    |42.0|34813|1.0|6969|0.2002|8.5|7642|0.2195|6.3|
    |42.5|35309|1.1|7137|0.2021|8.8|8257|0.2338|8.3|
    |43.0|34423|1.1|7513|0.2183|12.4|5919|0.1719|11.7|
    |43.5|34618|0.9|6059|0.1750|10.1|6379|0.1843|5.2|
    |44.0|34829|0.7|6003|0.1724|5.3|6014|0.1727|7.5|
    |44.5|34814|0.7|6139|0.1763|8.9|5398|0.1551|10.7|
    |45.0|34723|0.5|6179|0.1780|6.0|6092|0.1754|6.5|
    
