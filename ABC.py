import numpy as np
import copy
from TestFunc import TestFunc

# ABC sınıfı oluşturuluyor


class ABC:

    # Default parametreler
    def __init__(self, test_func, repeat=100, maxit=100, npop=20, nvar=20):

        self.costfunc = test_func.costfunc
        self.varmin = test_func.varmin
        self.varmax = test_func.varmax
        self.repeat = repeat
        self.maxit = maxit
        self.npop = npop
        self.nvar = nvar
        self.nonlookerpop = npop
        self.L = self.npop * self.nvar  # failure limit
        self.a = 1

    # ABC çalıştırılıyor
    def run(self):
        for rpt in range(self.repeat):

            # Boş bireyler oluşturuluyor
            empty_bee = {}
            empty_bee["position"] = None
            empty_bee["cost"] = None

            # En iyi çözümü tutan dictionary
            bestsol = empty_bee
            bestsol["cost"] = np.inf
            # İlk popülasyon rasgele oluşturuluyor
            pop = [0] * self.npop

            for i in range(self.npop):
                pop[i] = {}
                pop[i]["position"] = np.random.uniform(self.varmin, self.varmax, self.nvar)
                pop[i]["cost"] = self.costfunc(pop[i]["position"])
                # En iyi çözüm (gerekliyse) güncelleniyor
                if pop[i]["cost"] < bestsol["cost"]:
                    bestsol = copy.deepcopy(pop[i])

            # maxit boyutunda dizi tanımlanıyor (en iyi çözümlerin sonuçları tutulacak)
            bestcost = np.empty(self.maxit)

            # Failure counter
            fc = np.zeros(self.npop, int)

            # Recruited Bees
            for it in range(self.maxit):
                for i in range(self.npop):
                    # Choose k randomly, not equal to i
                    K = np.random.permutation(self.npop)
                    X = np.where(K == i)
                    K = np.delete(K, X)
                    k = K[0]
                    # Define Acceleration Coefficient
                    phi = np.random.uniform(-1, 1, self.nvar)
                    newbee = {}
                    # New Bee Position
                    newbee["position"] = pop[i]["position"] + phi * (pop[i]["position"] - pop[k]["position"])
                    # Apply Bounds
                    newbee["position"] = self.apply_bound(newbee["position"], self.varmin, self.varmax)
                    # Evaluation
                    newbee["cost"] = self.costfunc(newbee["position"])
                    # Comparision
                    if newbee["cost"] <= pop[i]["cost"]:
                        pop[i] = newbee.copy()
                    else:
                        fc[i] += 1
                # Calculate Fitness Values and Selection Probabilities
                F = np.zeros(self.npop)
                totalcost = 0
                for i in range(self.npop):
                    totalcost += pop[i]["cost"]
                meancost = totalcost / self.npop
                for i in range(self.npop):
                    F[i] = np.exp(-pop[i]["cost"]/meancost)
                P = F / np.sum(F)

                # Onlooker bees
                for m in range(self.nonlookerpop):
                    # Select Source Site
                    i = self.roulette_wheel_selection(P)
                    # Choose k randomly, not equal to i
                    K = np.random.permutation(self.npop)
                    X = np.where(K == i)
                    K = np.delete(K, X)
                    k = K[0]
                    # Define Acceleration Coefficient
                    phi = np.random.uniform(-1, 1, self.nvar)
                    newbee = {}
                    # New Bee Position
                    newbee["position"] = pop[i]["position"] + phi * (pop[i]["position"] - pop[k]["position"])
                    # Apply Bounds
                    newbee["position"] = self.apply_bound(newbee["position"], self.varmin, self.varmax)
                    # Evaluation
                    newbee["cost"] = self.costfunc(newbee["position"])
                    # Comparision
                    if newbee["cost"] <= pop[i]["cost"]:
                        pop[i] = newbee.copy()
                    else:
                        fc[i] += 1

                # Scout Bees
                for i in range(self.npop):
                    if fc[i] >= self.L:
                        pop[i]["position"] = np.random.uniform(self.varmin, self.varmax, self.nvar)
                        pop[i]["cost"] = self.costfunc(pop[i]["position"])
                        fc[i] = 0
                # Update Best Solution Ever Found
                for i in range(self.npop):
                    if pop[i]["cost"] < bestsol["cost"]:
                        bestsol = pop[i].copy()
                bestcost[it] = bestsol["cost"]
                print(it)
                print("\t")
                print(bestsol["cost"])
        # Elde edilen çıktılar döndürülüyor
        out = {}
        out["pop"] = pop
        out["bestsol"] = bestsol
        out["bestcost"] = bestcost
        # out["bests"] = bests
        return out

        # Çözümleri problem uzayında tutan metot

    def apply_bound(self, x, varmin, varmax):
        min = np.zeros(self.nvar)
        min.fill(varmin)
        max = np.zeros(self.nvar)
        max.fill(varmax)
        x = np.maximum(x, min)
        x = np.minimum(x, max)
        return x

    def roulette_wheel_selection(self, p):
        c = np.cumsum(p)
        r = sum(p)*np.random.rand()
        ind = np.argwhere(r <= c)
        return ind[0][0]