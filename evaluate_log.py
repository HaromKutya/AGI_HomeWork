import pandas as pd


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
