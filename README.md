
# Markov Chains and Limit Order Execution

A small mathematical project investigating when placing a limit order might be preferable to buying immediately using a market order.

The project uses a discrete-time absorbing Markov chain to model the position of a buy order in a queue. The aim is to calculate the probability of execution, the expected waiting time, and the expected cost of placing a limit order.

## Write-up

The full mathematical explanation, derivations and numerical examples can be found in [writeup.pdf](writeup.pdf).

## Limitations

This is a very simplified model. The transition probabilities are hypothetical rather than estimated from market data. The model also makes several assumptions about how orders move through the queue. The main aim is to demonstrate an application of Markov chain theory to a problem involving financial markets.

## Sources and References

The results in Markov chain theory which were applied are some of those in *Grimmett and Welsh's Probability: An Introduction*. The notes I made while studying this book can be found in [probability_notes.pdf](probability_notes.pdf).

The idea for the project - that is, to use Markov chain theory to model an order book - came from the much more advanced examples in *Cont, Stoikov, and Talreja's A Stochastic Model for Order Book Dynamics*, which introduce far more applicable (and harder to understand!) models in continuous time.

*AI Disclosure*: An LLM was used to provide specific numerical examples which would lead to interesting results and proof-read the writeup for errors and issues in LaTeX formatting. It also helped with debugging code when there were some more obscure errors. Finally, an LLM suggested the addition of the additional interpretation of the matrix $(I-Q)^{-1}$ in the section on expected waiting times and the graphical outputs of the program to the writeup.
