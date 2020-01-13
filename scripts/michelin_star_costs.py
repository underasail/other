
import csv
from matplotlib import pyplot as plt

files = ['one-star-michelin-restaurants.csv', 
         'two-stars-michelin-restaurants.csv',
         'three-stars-michelin-restaurants.csv']
plot_data_1 = []
plot_data_2 = []
plot_data_3 = []
plots = [plot_data_1, plot_data_2, plot_data_3]
for file, plot_data in zip(files, plots):
    costs = []
    with open(file, 'r') as f:
        csvreader = csv.reader(f, delimiter = ',')
        for row in csvreader:
            cost = row[8]
            if '$' not in cost:
                pass
            else:
                costs.append(cost.count('$'))
    
        c_end = max(costs)
#        plot_data = []
        signs = range(1, c_end + 1)
        for i in signs:
            plot_data.append(costs.count(i))

fig, ax = plt.subplots()

plt.plot(signs, plot_data_1, label = 'One-star')
plt.plot(signs, plot_data_2, label = 'Two-stars')
plt.plot(signs, plot_data_3, label = 'Three-stars')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.xticks(signs, ('$', '\$$', '$$$', '\$$$$', '$$$$$'))
plt.xlabel('Price Range')
plt.ylabel('Number of Restaurants')
plt.title('Worldwide Michelin Guide Restaurant Pricing\n')

plt.legend()

#plt.show()
plt.savefig('Michelin_Star_Costs.png', bbox_inches = 'tight', format = 'png', 
            dpi = 600)

#%%