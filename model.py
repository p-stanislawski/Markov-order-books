
import numpy as np
import matplotlib.pyplot as plt


# This function works out the probabilities, waiting times and costs
# d is the list of probabilities of moving forward in the queue
# a is the probability of an adverse price movement
# delta is how much the ask goes up if that happens

def calculate(d, a, delta):
    n = len(d)  # number of queue positions (0, 1, ..., n-1)

    # Q is for moving between queue positions
    # R is for going to one of the absorbing states F or A
    Q = np.zeros((n, n))
    R = np.zeros((n, 2))

    # Fill in the matrices one row at a time
    for q in range(n):
        Q[q, q] = 1 - d[q] - a  # nothing changes
        R[q, 1] = a             # price moves against us

        if q == 0:
            R[q, 0] = d[q]      # our order gets filled
        else:
            Q[q, q - 1] = d[q]  # one fewer order ahead of us

    # Work out I-Q, which appears in both of our equations
    M = np.eye(n) - Q

    # First solve (I-Q)h=r to get the fill probabilities
    h = np.linalg.solve(M, R[:, 0])

    # Then solve (I-Q)t=1 to get the expected times
    t = np.linalg.solve(M, np.ones(n))

    # The other absorbing outcome has probability 1-h
    # Work out the expected cost of starting with a limit order
    cost = 99.99 * h + (100.01 + delta) * (1 - h) + 0.001 * t

    return h, t, cost


# Now there can be as many as 3 orders ahead of ours
# The first three values are the ones from the write-up
# We have chosen d_3=0.20 for the extra position

d = [0.40, 0.30, 0.25, 0.20]
a = 0.10
delta = 0.01

h, t, costs = calculate(d, a, delta)

# Print the answers for the main example
print("Market order cost: $100.0100")
print("Results for a fixed price increase of $0.01:")

for q in range(len(d)):
    print("q =", q)
    print("  Probability of execution:", round(h[q], 4))
    print("  Expected time:", round(t[q], 4))
    print("  Expected cost: $", format(costs[q], ".4f"), sep="")

    if costs[q] < 100.01:
        print("  Limit order is cheaper")
    else:
        print("  Market order is cheaper")


# The break-even increase in the ask, from our formula
print("\nBreak-even price increases:")

for q in range(len(d)):
    value = (h[q] * 0.02 - 0.001 * t[q]) / (1 - h[q])
    print("q =", q, ": delta <", round(value, 4))


# We can also let the price increase be random
# Here it is $0.01 with probability 3/4 and $0.03 with probability 1/4
# Because we only want the expected cost, we just use E(D)

mean_delta = 0.75 * 0.01 + 0.25 * 0.03
h2, t2, random_costs = calculate(d, a, mean_delta)

print("\nRandom price increase, with mean", round(mean_delta, 4))

for q in range(len(d)):
    print("q = ", q, " : expected cost = $",
          format(random_costs[q], ".4f"), sep="")


# Check that our answers agree with the product formula we derived
print("\nProbabilities from the product formula:")

answer = 1

for q in range(len(d)):
    answer = answer * d[q] / (d[q] + a)
    print("q =", q, ":", round(answer, 4))


# First graph: how the fill probability changes with a
positions = range(len(d))

for a in [0.05, 0.10, 0.20]:
    h, t, costs = calculate(d, a, delta)
    plt.plot(positions, h, marker="o", label="a = " + str(a))

plt.xlabel("Number of orders ahead")
plt.ylabel("Probability of execution")
plt.title("Probability of execution")
plt.xticks(list(positions))
plt.ylim(0, 1)
plt.legend()
plt.tight_layout()
plt.savefig("fill_probabilities.png", dpi=200)
plt.close()


# Second graph: compare the costs of limit and market orders
# Below zero means the limit order is cheaper

for a in [0.05, 0.10, 0.20]:
    h, t, costs = calculate(d, a, delta)
    plt.plot(positions, costs - 100.01, marker="o",
             label="a = " + str(a))

plt.axhline(0, color="black", linestyle="--")
plt.xlabel("Number of orders ahead")
plt.ylabel("Limit cost minus market cost ($/share)")
plt.title("Expected cost difference")
plt.xticks(list(positions))
plt.legend()
plt.tight_layout()
plt.savefig("execution_costs.png", dpi=200)
plt.close()
