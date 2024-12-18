import random
import math
import time
import matplotlib.pyplot as plt
import csv

city = []
#city = [[chr(0),1,1,''],[chr(1),1,2,''],[chr(2),1,3,''],[chr(3),1,4,''],[chr(4),1,5,''],[chr(5),1,6,''],[chr(6),2,6,''],[chr(7),3,6,''],[chr(8),4,6,''],[chr(9),5,6,''],[chr(10),6,6,''],[chr(12),6,5,''],[chr(13),6,4,''],[chr(14),6,3,''],[chr(15),6,2,''],[chr(16),6,1,''],[chr(17),5,1,''],[chr(18),4,1,''],[chr(19),3,1,''],[chr(20),2,1,'']]



class TspGeneticAlgorithm:

    #Function for creating random data
    def CreateRandomData(self,xrange,yrange, city_num):
        for i in range (city_num):
            x = random.randrange(1,xrange)
            y = random.randrange(1,yrange)
            city.append((chr(i), x, y))

    #Function for reading data
    def ReadData(self):
        f = open('data.csv', 'r', encoding='utf-8') #data.csv contains the longtitude and latitude of cities in South Korea
        rdr = csv.reader(f)
        cnt = -1
        city_name = ""
        city_lat = 0  # latitude
        city_longt = 0  # longtitude
        for line in rdr:
            if rdr.line_num % 3 == 1:
                city_name = line[0]
                cnt += 1
            if rdr.line_num % 3 == 0:
                city_longt = round(float(line[0][:8]), 2)
                city_lat = round(float(line[0][9:]), 2)
                city.append((chr(cnt), city_lat, city_longt, city_name))

        f.close()

    
    def __init__(self, n):
        # Selection of data
        
        # 1) Random Generated Data
        # self.CreateRandomData(100, 100, 20)
        # 2) Data from data.csv
        self.ReadData()

        self.n = n
        self.generation = 0
        self.chromosomes = []
        self.fitlist = []
        self.city_distance = [[0]*len(city) for i in range(len(city))] # list of distance between the cities
        self.cur_gen = 0 #current generation
        self.total_gen = 5000 #total generation to evolve

        #Implementing a nested list containing the distance between cities
        for i in range(len(city)):
            for j in range(len(city)):
                x = city[i][1] - city[j][1]
                y = city[i][2] - city[j][2]
                distance = math.sqrt((x * x) + (y * y)) # distance by pytagorean theorem
                self.city_distance[i][j] = round(distance,2)

        #Creating a random route for the first generation
        check1 = [0 for i in range(len(city))]
        for i in range(n):
            chromosome = ''
            check1 = [0 for i in range(len(city))]

            for j in range(len(city)):
                while(1):
                    rand_sel = random.randrange(0,len(city)) # selects a random city
                    if check1[rand_sel] == 0:
                        check1[rand_sel] = 1
                        break
                chromosome += city[rand_sel][0]
            self.chromosomes.append((chromosome, self.evaluation(chromosome))) # making a random route for the first generation

        self.chromosomes.sort(key=lambda x:x[1], reverse=False) # sorting the route

    #Evaulation function for fitness
    def evaluation(self, chromosome):
        sum = 0
        for i in range(len(city) - 1):
            idx1 = ord(chromosome[i])
            idx2 = ord(chromosome[i+1])
            sum += self.city_distance[idx1][idx2] #Adds the distances following the route
        idx1 = ord(chromosome[0])
        idx2 = ord(chromosome[len(city)-1])
        sum += self.city_distance[idx1][idx2]
        return sum


    #Roulette Wheel Selection
    def roulette_wheel_selection(self):
        check2 = [0 for i in range(len(city))]
        fit_total = 0
        for i in self.chromosomes:
            fit_total += i[1]

        roulette_pos = 0
        chromosome_sel = [-1,-1]
        chromosome_cnt = 0
        
        while chromosome_cnt != 2: #Loops until two chromosomes are selected
            pos = 0
            roulette_pos = random.uniform(0, fit_total) #Random selection of chromosome
            for i in range(len(self.chromosomes)): #iterates until the roullete position reaches the random selected chromosome
                pos += self.chromosomes[i][1] 
                if roulette_pos <= pos and not check2[i]: 
                    chromosome_sel[chromosome_cnt] = i
                    chromosome_cnt += 1
                    check2[i] = 1 #Prevent re-selection of the same chromosome
                    break

        return self.chromosomes[chromosome_sel[0]],self.chromosomes[chromosome_sel[1]]

    #Elite Preserving Selection
    def elitist_preserving_selection(self):
        return self.chromosomes[0] #returns the best fit chromosome

    #Single Point Crossover
    def single_point_crossover(self, chromosome1, chromosome2):
        pivot = random.randint(1,len(chromosome1) - 1) #selects the point for crossover
        idx = pivot
        offspring = chromosome1[:pivot]
        while len(offspring) != len(city):
            tmp = 0
            for i in range(len(offspring)):
                if chromosome2[idx] != offspring[i]:
                    tmp += 1
            if(tmp == len(offspring)):
                offspring += chromosome2[idx]
            idx = (idx+1) % len(city)

        offspring = self.static_mutation(offspring,0.05) # casts mutation by 5% chance
        return offspring

    def static_mutation(self, chromosome, p):
        result = ''
        pivot1 = pivot2 = 0
        r = random.random()
        if r <= p:
            print('Mutation')
            pivot1 = random.randint(0,len(city)-1) # selecting the two random points to be swapped
            pivot2 = random.randint(0,len(city)-1)
            while pivot1 == pivot2:
                pivot2 = random.randint(0, len(city) - 1)

        for i in range(len(chromosome)): #swapping the two pivot points
            if i == pivot1:
                result += chromosome[pivot2]
            elif i == pivot2:
                result += chromosome[pivot1]
            else:
                result += chromosome[i]
                
        return result 


    #Evolution
    def evolution(self):
        temp_chromosomes = []
        chromosome1 = self.elitist_preserving_selection() #selects one chromosome by elite preserving selection
        temp_chromosomes.append((chromosome1[0],self.evaluation(chromosome1[0])))
        for i in range(self.n - 1):
            chromosome1, chromosome2 = self.roulette_wheel_selection() # selects two chromosomes with Roullete wheel selection
            offspring = self.single_point_crossover(chromosome1[0],chromosome2[0]) #Produces offspring by single point crossover
            temp_chromosomes.append((offspring, self.evaluation(offspring)))

        temp_chromosomes.sort(key=lambda x: x[1], reverse=False)
        self.chromosomes = temp_chromosomes #appends chromosomes of the next generation
        self.generation += 1


    def record_fit(self):
        self.fitlist.append(self.chromosomes[0][1])

    def train(self):
        print(self)
        self.record_fit()
        last = 0
        now = 0
        cnt = 0
        while True:
            last = now
            self.evolution()
            now = self.chromosomes[0][1]
            self.record_fit()
            print(self)
            self.cur_gen += 1
            if last == now:
                cnt += 1
            else:
                cnt = 0
            if cnt > 1000:
                break

    def showmap(self):
        minx = miny = 200
        maxx = maxy = 0
        for i in range(len(city)):
            if city[i][1] < minx:
                minx = city[i][1]
            if city[i][2] < miny:
                miny = city[i][2]
            if city[i][1] > maxx:
                maxx = city[i][1]
            if city[i][2] > maxy:
                maxy = city[i][2]
        a = [city[x][1] for x in range(0, len(city))]
        b = [city[y][2] for y in range(0, len(city))]
        plt.plot(a, b, '.')
        plt.axis([minx - 1, maxx + 1, miny - 1, maxy + 1])
        plt.show()

    def showplot(self):
        plt.figure(0)
        plt.plot(self.fitlist)
        plt.show()

    def getRoute(self, chromosome):
        a = []
        b = []
        for i in range(len(city)):
            a.append(city[ord(chromosome[i])][1])
            b.append(city[ord(chromosome[i])][2])
            if(i * 2 == len(city)):
                print()
        a.append(city[ord(chromosome[0])][1])
        b.append(city[ord(chromosome[0])][2])
        return a,b

    def showRoute(self):

        plt.figure(figsize=(12, 7))
        plt.subplot(1, 2, 1)
        minx = miny = 200
        maxx = maxy = 0
        for i in range(len(city)):
            if city[i][1] < minx:
                minx = city[i][1]
            if city[i][2] < miny:
                miny = city[i][2]
            if city[i][1] > maxx:
                maxx = city[i][1]
            if city[i][2] > maxy:
                maxy = city[i][2]
        plt.axis([minx - 1, maxx + 1, miny - 1, maxy + 1])
        a, b = self.getRoute(self.chromosomes[0][0])
        plt.plot(a, b, color="g", marker="o", markerfacecolor="r", linestyle=":")
        plt.subplot(1, 2, 2)
        plt.plot(self.fitlist)
        plt.ylabel('Distance')
        plt.xlabel('Generation')
        plt.title('Genetic Algorithm')
        plt.show()

    def __str__(self):
        ret = '=== Generation' + str(self.generation) + '===\n'
        ret +='(Overall Fitness) : ' + str(self.chromosomes[1]) + '\n'
        return ret

if __name__ == "__main__":
    TGA = TspGeneticAlgorithm(5)
    
    #Route before training
    TGA.showRoute()
    
    TGA.train()
    #Route after training
    TGA.showRoute()