import matplotlib.pyplot as plt

x = [5000,10000,15000,20000,25000,30000,35000,40000]

y = [0.108258344342797,0.0814367973676995,0.0702943889124311,0.0655831692300023,0.0612707829598425,0.0571827404840841,0.0559862402472767,0.0540917815389984]

plt.plot(x, y)

plt.xlabel('Number of sentences trained with')

plt.ylabel('Error rate by Word')

plt.title('Learning Curve by Siyuan Yao')

plt.show()
