import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


opponent_dict = {
    1: "RandomAgent",
    2: "CentroidRandomAgent",
    3: "GreedyRandomAgent",
    4: "MinimalistRandomAgent"
}

log_path = "training_log_1608130275.csv"

data = pd.read_csv(log_path)

data_against_random = data[data["opponent"] != 0]

victories_against_random = data_against_random[data_against_random["starting_player"] == data_against_random["winner"]].shape[0]
ties_against_random = data_against_random[data_against_random["winner"] == -1].shape[0]
losses_against_random = data_against_random.shape[0] - (victories_against_random + ties_against_random)

print("Victories against random: %.4f" % (float(victories_against_random) / float(data_against_random.shape[0])))
print("Ties against random: %.4f" % (float(ties_against_random) / float(data_against_random.shape[0])))
print("Losses against random: %.4f" % (float(losses_against_random) / float(data_against_random.shape[0])))

for i in range(1, len(opponent_dict) + 1):
    games = data_against_random[data_against_random["opponent"] == i]
    victories = games[games["starting_player"] == games["winner"]].shape[0]
    ties = games[games["winner"] == -1].shape[0]
    losses = games.shape[0] - (victories + ties)

    print("\nVictories against " + opponent_dict[i] + ": %.4f" % (float(victories) / float(games.shape[0])))
    print("Ties against " + opponent_dict[i] + ": %.4f" % (float(ties) / float(games.shape[0])))
    print("Victories against " + opponent_dict[i] + ": %.4f" % (float(losses) / float(games.shape[0])))

print("\nStarting player winning rate: %.4f" % (float(data[data["winner"] == 1].shape[0]) / float(data.shape[0])))


x = data_against_random.index.values

y = []
for i in range(len(x)):
    lower_bound = i - 2000
    if lower_bound < 0:
        lower_bound = 0
    current_data = data_against_random[lower_bound:i]
    victories = current_data[current_data["starting_player"] == current_data["winner"]].shape[0]
    if current_data.shape[0] > 0:
        win_rate = float(victories) / float(current_data.shape[0])
    else:
        win_rate = 0.
    y.append(win_rate)

y = np.array(y)

plt.plot(x, y)
plt.ylim((0, 1))
plt.title("Against all random agents (window size: 2000)")
plt.xlabel("All games played")
plt.ylabel("Win ratio for the last 2000 games")
plt.show()


for i in range(1, len(opponent_dict) + 1):
    games = data_against_random[data_against_random["opponent"] == i]

    x = games.index.values

    y = []
    for j in range(len(x)):
        lower_bound = j - 200
        if lower_bound < 0:
            lower_bound = 0
        current_data = games[lower_bound:j]
        victories = current_data[current_data["starting_player"] == current_data["winner"]].shape[0]
        if current_data.shape[0] > 0:
            win_rate = float(victories) / float(current_data.shape[0])
        else:
            win_rate = 0.
        y.append(win_rate)

    y = np.array(y)

    plt.plot(x, y)
    plt.ylim((0, 1))
    plt.title("Against " + opponent_dict[i] + " (window size: 200)")
    plt.xlabel("All games played")
    plt.ylabel("Win ratio for the last 200 games")
    plt.show()
