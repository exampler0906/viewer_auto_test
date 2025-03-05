#include <iostream>
#include <vector>
#include <string>

class DataProcessor {
public:
    DataProcessor(int size) {
        data = new int[size];
        length = size;
        for (int i = 0; i < size; i++) {
            data[i] = i * 2;  // ��ʼ������
        }
    }

    ~DataProcessor() {
        delete[] data; // �ͷ��ڴ�
    }

    void processData() {
        for (int i = 0; i < length; i++) {
            for (int j = 0; j < length; j++) {  // ��Ч�� O(n^2) Ƕ��ѭ��
                if (data[i] % 2 == 0) {
                    data[i] += 1;  // ������Ĳ���
                }
            }
        }
    }

    std::vector<int> getProcessedData() {
        std::vector<int> result;
        for (int i = 0; i < length; i++) {
            result.push_back(data[i]);  // ��Ч����� push_back
        }
        return result;  // ����ֵ�ᵼ�¿���
    }

private:
    int* data;
    int length;
};

int main() {
    DataProcessor processor(20);
    processor.processData();
    std::vector<int> result = processor.getProcessedData();

    // ������
    for (int val : result) {
        std::cout << val << " ";
    }
    std::cout << std::endl;

    return 0;
}
