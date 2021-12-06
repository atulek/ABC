# Gerekli kütüphaneler ile PSO ve GA sınıfları ekleniyor
from ABC import ABC
from TestFunc import TestFunc
import matplotlib.pyplot as plt

# ABC Default parametreleri
abc = ABC(
    test_func=TestFunc().Sphere(),
    repeat=1,
    maxit=1000,
    npop=50,
    nvar=50
)

pop, bestsol, bestcost = abc.run().values()
#result = de.run()
# print(bests)

# Optimum ABC sonuç grafiği çizdiriliyor
plt.semilogy(bestcost)
plt.xlim(0, 1000)
plt.xlabel('İterasyonlar')
plt.ylabel('Maliyet Fonksiyonu')
plt.title('Artificial Bee Colony (ABC)')
plt.grid(True)
plt.show()

