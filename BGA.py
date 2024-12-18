import random
import time
import matplotlib.pyplot as plt


class BinaryGeneticAlgorithm:
    # 랜덤으로 초기집단 염색체 생성 후 적합도 평가
    def __init__(self, n):
        self.n = n
        self.generation = 0
        self.chromosomes = []
        self.fitlist = []

        for i in range(n):
            chromosome = ''
            for j in range(4):
                if random.random() <= 0.5:
                    chromosome += '0'
                else:
                    chromosome += '1'
            self.chromosomes.append((chromosome, self.evaluation(chromosome)))
        self.chromosomes.sort(key=lambda x: x[1], reverse=True)

    # 적합도를 계산하는 평가 함수
    def evaluation(self, chromosome):
        return int(chromosome, 2)

    # 룰렛 휠을 이용한 선택 연산
    # 각 염색체가 선택될 확률 = (염색체의 적합도 / 모든 염색체의 적합도 총합)
    def roulette_wheel_selection(self):
        fit = []
        for i in self.chromosomes:
            if len(fit) == 0:
                fit.append(i[1])
            else:
                fit.append(fit[-1] + i[1])
        roulette_pos = 0
        roulette_pos = random.randint(0, fit[-1])

        chromosome1 = -1
        chromosome2 = -1
        pos = 0
        for i in range(len(self.chromosomes)):
            pos += self.chromosomes[i][1]
            if roulette_pos <= pos:
                chromosome1 = i
                break

        while chromosome2 == -1 or chromosome2 == chromosome1:
            pos = 0
            roulette_pos = random.randint(0, fit[-1])
            for i in range(len(self.chromosomes)):
                pos += self.chromosomes[i][1]
                if roulette_pos <= pos:
                    chromosome2 = i
                    break

        return self.chromosomes[chromosome1], self.chromosomes[chromosome2]

    # 교차를 이용한 교배 연산
    def single_point_crossover(self, chromosome1, chromosome2):
        pivot = random.randint(1, len(chromosome1) - 1)
        offspring = chromosome1[:pivot] + chromosome2[pivot:]
        return offspring

    # 진화 수행
    def evolution(self):
        temp_chromosomes = []
        for i in range(self.n):
            chromosome1, chromosome2 = self.roulette_wheel_selection()
            offspring = self.single_point_crossover(chromosome1[0], chromosome2[0])
            temp_chromosomes.append((offspring, self.evaluation(offspring)))

        temp_chromosomes.sort(key=lambda x: x[1], reverse=True)
        self.chromosomes = temp_chromosomes
        self.generation += 1

    def record_fit(self):
        # self.fit_avg.append(sum([i[1] for i in self.chromosomes])/len(self.chromosomes))
        self.fitlist.append(self.chromosomes[0][1])

    def train(self):
        print(self)
        self.record_fit()

        check = 0

        while True:
            self.evolution()
            self.record_fit()
            print(self)
            time.sleep(0.01)
            check += 1
            if check == 300:
                break

    def showplot(self):
        plt.figure(0)
        plt.plot(self.fitlist)
        plt.show()

    def __str__(self):
        ret = '=== ' + str(self.generation) + '세대 ===\n'
        ret += '(염색체, 적합도) : ' + str(self.chromosomes) + '\n'
        return ret


if __name__ == "__main__":
    # 한 집단의 개체 수(4)
    BGA = BinaryGeneticAlgorithm(4)
    BGA.train()