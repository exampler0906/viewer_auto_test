#include <iostream>
#include <vector>
#include <string>

class DataProcessor {
public:
    DataProcessor(int size) {
        data = new int[size];
        length = size;
        for (int i = 0; i < size; i++) {
            data[i] = i * 2;  // 初始化数据
        }
    }

    ~DataProcessor() {
        delete[] data; // 释放内存
    }

    void processData() {
        for (int i = 0; i < length; i++) {
            for (int j = 0; j < length; j++) {  // 低效的 O(n^2) 嵌套循环
                if (data[i] % 2 == 0) {
                    data[i] += 1;  // 无意义的操作
                }
            }
        }
    }

    std::vector<int> getProcessedData() {
        std::vector<int> result;
        for (int i = 0; i < length; i++) {
            result.push_back(data[i]);  // 低效的逐个 push_back
        }
        return result;  // 返回值会导致拷贝
    }

private:
    int* data;
    int length;
};

int main() {
    DataProcessor processor(20);
    processor.processData();
    std::vector<int> result = processor.getProcessedData();

    // 输出结果
    for (int val : result) {
        std::cout << val << " ";
    }
    std::cout << std::endl;

    return 0;
}
