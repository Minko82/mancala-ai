# ♟️ Mancala AI

A command-line Mancala game powered by AI using **Minimax** and **Alpha-Beta Pruning**, with configurable search depth for adjustable difficulty.

---

### 📊 100-Game Simulation Mode
Benchmark AI performance through automated simulations that reveal strategic strength over time.

| Player 1                         | Player 2                         | Depth (Plies) | Games | Description                        |
|----------------------------------|----------------------------------|----------------|--------|------------------------------------|
| `random_player`                  | `random_player`                  | –              | 100    | Baseline comparison of randomness |
| `minimax_player_with_variable_plies(5)` | `random_player`         | 5              | 100    | Minimax vs random                 |
| `alpha_beta_player_with_variable_plies(5)` | `random_player`      | 5              | 100    | Alpha-Beta vs random              |
| `alpha_beta_player_with_variable_plies(10)` | `random_player`     | 10             | 100    | Deeper Alpha-Beta vs random       |
| `minimax_player_with_variable_plies(5)` | `alpha_beta_player_with_variable_plies(5)` | 5 | 100 | Minimax vs Alpha-Beta             |


<br>

#### To Run Simulation: 
```
  python mancala_ai.py
```
---

### 📈 Statistical Analysis
At the end of each simulation, the program outputs win rates, average move counts, and tie frequency — offering insight into each AI’s performance.

<p align="center">
  <img width="341" height="86" alt="Statistics Screenshot" src="https://github.com/user-attachments/assets/132d90f9-2b84-4478-a5b3-58e0b67faa30" />
</p>

---

### 🧠 Powered by AIMA
Built on [AIMA’s](https://github.com/aimacode/aima-python) adversarial search framework.
