# jsonTool

## insertKVPair

可以使用`insertKVPair className(QString srcStr)`实例化一个类名为`className`的类，`srcStr`是从输入框中读取的`QString `，类中的主要成员函数为：

1. `QJsonObject getJsonObj()`

    直接返回类中的成员变量`m_obj`；

2. `void insertKVPairInEveryDepth()`

    在`QJsonObject`的所有层级下，插入一个合法的键值对；

3. `void randomInsertKVPairInRandomDepth(double stopProbability = 0.6);`

    在QJsonObject的随机层级下，插入一个合法的键值对，`stopProbability`停止概率，当小于该概率时，直接在当前层级下插入，否则继续遍历。

## compareJson

可以使用`compareJson className(QString srcStr1, QString srcStr2)`实例化一个类名为`className`的类，`srcStr1`和`srcStr2`是从输入框中读取的两个欲进行比较的`QString`，类中的主要成员函数为：

1. `QJsonObject getJsonObj1()`

    直接返回类中的成员变量`m_obj1`；

2. `QJsonObject getJsonObj2()`

    直接返回类中的成员变量`m_obj2`；

3. `int compare()`

    返回一个`int`，可能的返回值如下：

    - 0：两`json`相等
    - 1：`json1`是`json2`的子集
    - 2：`json2`是`json1`的子集
    - 3：`json1`中存在`json2`中没有的键值对
    - 4：`json2`中存在`json1`中没有的键值对

    其中`json1`和`json2`分别指`srcStr1`和`srcStr2`代表的`QJsonObject`。

