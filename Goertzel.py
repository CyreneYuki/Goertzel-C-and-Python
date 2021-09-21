import copy
import math


class Goertzel:
    def __init__(self, interval, res, point, rate, input_list):  # 频率间隔，谐波次数，数据长度，采样率，数据
        self.interval = interval
        self.input_list = input_list
        self.res = res
        self.point = point
        self.rate = rate
        self.P = [0] * res
        # 初始化参数
        Q0, Q1, Q2, C, f, temp, k = [0] * self.res, [0] * self.res, [0] * self.res, [], [], [], []
        for i in range(0, self.res):
            f.append(self.interval * (i + 1))
            k.append(round((self.point * f[i]) / self.rate))  # 采样率3200
            temp.append((2 * math.pi * k[i]) / self.point)  # K=N*f/R
            C.append(2 * (math.cos(temp[i])))  # w=3.141593*2*K/N(弧度)
        # 计算
        for j in range(0, self.point):
            for i in range(0, self.res):  # 计算Q0
                Q0[i] = C[i] * Q1[i] - Q2[i] + self.input_list[j]
            Q2 = copy.deepcopy(Q1)
            Q1 = copy.deepcopy(Q0)
        # 计算完毕，全部谐波求模
        for i in range(0, self.res):
            self.P[i] = Q1[i] * Q1[i] + Q2[i] * Q2[i] - C[i] * Q1[i] * Q2[i]  # 若数据过大容易溢出，开根号/取对数/右移

    def output(self):
        print(self.P)

    """
    # 计算单个谐波向量
    def several(self, input_list, order):
        Q1_alone = Q2_alone = 0  # 清零
        j = 0
        while j < N:
            data = input_list[j]  # int提升为float；
            Q0_alone = C[order - 1] * Q1_alone - Q2_alone + data
            Q2_alone = Q1_alone
            Q1_alone = Q0_alone
            j += 1
        # 计算完毕，求模
        P1 = Q1_alone * Q1_alone + Q2_alone * Q2_alone - C[order - 1] * Q1_alone * Q2_alone
        return P1
    """


# 获得数据
def data_set(frequency, rate, N):  # 频率，采样率，采样点数
    x = []
    for i in range(0, N):
        x.append(220 * math.sin(i * frequency * 2 * math.pi / rate))
    return x


if __name__ == '__main__':
    wave1 = data_set(50, 3200, 64)
    g1 = Goertzel(50, 5, 64, 3200, wave1)
    g1.output()
    g2 = Goertzel(50, 3, 128, 3200, data_set(100, 3200, 128))
    # g2.init()
    g2.output()
    g1.output()
