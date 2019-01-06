## 算法来源

算法来自于论文Clustering by fast search and find of density peaks，在实现过程中对博客 https://www.cnblogs.com/peghoty/p/3945653.html 和 https://blog.csdn.net/jdplus/article/details/40351541 进行了一定参考
## 数据来源
测试所用的数据来自于一个叫做Clustering basic benchmark的网站（http://cs.joensuu.fi/sipu/datasets/）， 在网站中选取了Shape Sets下的几个数据集进行测试。
该组数据集中数据为2维，并且包含了真实的聚类结果。
数据集的具体信息如下：

|数据集|长度|类别数|维数|来源|
| ------ | ------- | ------- | ------- | ------- |
|Aggregation|788|7|2| A. Gionis, H. Mannila, and P. Tsaparas, Clustering aggregation. ACM Transactions on Knowledge Discovery from Data (TKDD), 2007. 1(1): p. 1-30.|
|D31|3100|31|2|C.J. Veenman, M.J.T. Reinders, and E. Backer, A maximum variance cluster algorithm. IEEE Trans. Pattern Analysis and Machine Intelligence 2002. 24(9): p. 1273-1280|
|Flame|240|2|2|L. Fu and E. Medico, FLAME, a novel fuzzy clustering method for the analysis of DNA microarray data. BMC bioinformatics, 2007. 8(1): p. 3.|
|R15|600|15|2|C.J. Veenman, M.J.T. Reinders, and E. Backer, A maximum variance cluster algorithm. IEEE Trans. Pattern Analysis and Machine Intelligence, 2002. 24(9): p. 1273-1280. |
|Spiral|312|3|2|H. Chang and D.Y. Yeung, Robust path-based spectral clustering. Pattern Recognition, 2008. 41(1): p. 191-203. |

## 性能测试
算法来自于论文Clustering by fast search and find of density peaks，实现过程中将δ和ρ的乘积较大的点作为聚类中心实现聚类，实现了较好的聚类结果。不同数据集对应的结果都存放在“测评结果”文件夹下相应的目录下了,每个目录中有四张图片，分别是该组数据集的决策图、γ分步图、聚类结图和实际结果图。

### 测评结果

#### Aggregation
![Aggregation](https://github.com/TiYife/cluster/raw/master/Figure/Aggregation/决策图.png)
![Aggregation](https://github.com/TiYife/cluster/raw/master/Figure/Aggregation/γ.png)
![Aggregation](https://github.com/TiYife/cluster/raw/master/Figure/Aggregation/聚类结果图.png)
![Aggregation](https://github.com/TiYife/cluster/raw/master/Figure/Aggregation/实际类别图.png)


#### D31
![D31](https://github.com/TiYife/cluster/raw/master/Figure/D31/决策图.png)
![D31](https://github.com/TiYife/cluster/raw/master/Figure/D31/γ.png)
![D31](https://github.com/TiYife/cluster/raw/master/Figure/D31/聚类结果图.png)
![D31](https://github.com/TiYife/cluster/raw/master/Figure/D31/实际类别图.png)

#### Flame
![Flame](https://github.com/TiYife/cluster/raw/master/Figure/Flame/决策图.png)
![Flame](https://github.com/TiYife/cluster/raw/master/Figure/Flame/γ.png)
![Flame](https://github.com/TiYife/cluster/raw/master/Figure/Flame/聚类结果图.png)
![Flame](https://github.com/TiYife/cluster/raw/master/Figure/Flame/实际类别图.png)

#### R15
![R15](https://github.com/TiYife/cluster/raw/master/Figure/R15/决策图.png)
![R15](https://github.com/TiYife/cluster/raw/master/Figure/R15/γ.png)
![R15](https://github.com/TiYife/cluster/raw/master/Figure/R15/聚类结果图.png)
![R15](https://github.com/TiYife/cluster/raw/master/Figure/R15/实际类别图.png)

#### Spiral
![Spiral](https://github.com/TiYife/cluster/raw/master/Figure/Spiral/决策图.png)
![Spiral](https://github.com/TiYife/cluster/raw/master/Figure/Spiral/γ.png)
![Spiral](https://github.com/TiYife/cluster/raw/master/Figure/Spiral/聚类结果图.png)
![Spiral](https://github.com/TiYife/cluster/raw/master/Figure/Spiral/实际类别图.png)

γ分步和聚类结果图中的黑色点代表聚类中心，每一种颜色代表一个聚类（由于只选取10中颜色空间，不同聚类可能会有相同颜色）。

可以看出聚类之后的结果和数据集提供的数据有着较高的相似性。但是也有部分情况下由于没有事先声明类别数目，所有会有聚类数目和实际类别数目不符的情况，如Aggregation和Flame，但他们也提供了较好的聚类结果。
