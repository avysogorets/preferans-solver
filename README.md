## Preference (преферанс) solver.
---
### Introduction.
Preference is a popular Russian card game that gained its popularity in the early 19-th century. It is played with a French 32-card deck (7 to Ace) dealt for three hands of 10 cards each and a 2-card talon. In a nutshell, Preferance is a trick-taking game with the goal of fulfilling a declared contract, agreed upon by all players during the bidding stage. At this stage, players can bid to either (1) pass (2) play a game, or (3) play misere, leading to one of three types of contracts: (1) all-passes, (2) game, or (3) misere. All-passes occurs when all players pass and requires them to avoid taikng tricks, adding negative points for each trick taken. Let's talk about other contracts in more detail:
- *Game* is a contract where one player takes responsibility to take a declared number of tricks (no less than 6) under a major suit of his choice. The other players have an option to *whist*&mdash;contract themselves to take some or all of the remaining tricks. When exactly one player whists, he may choose to open up his and other player's cards, which is called "playing in the light". Ultimately, the player (and his opponents as a whole) are incentivized to take as many tricks as possible.
- *Misere* is a contract where one player obliges himself to take no tricks at all. The other two players open up their cards and try to force the other player to take as many tricks as possible. Misere is a rare and risky game with a lot at stake and hence is not played too often.

The complete set of rules of Preferans is sophisticated and has a great deal of nuances; you can read more [here](https://en.wikipedia.org/wiki/Preferans).

### The task

This program is not a robot-player preconditioned to maximize the returns, nor it is designed to produce optimal decisions for one of the players under incomplete information about the deal. On the other hand, it computes the outcome of the deal (the number of tricks taken by each player) assuming that *complete information* is available to all players (i.e., all cards open) and that they use it to *play optimally*. Optimal play is defined recursively: (1) it is optimal for a player with one card left to play it, and (2) it is optimal to play the card that leads to the most desirable outcome (according to the objective of the contract) assuming *optimal play* from the opponents. Note that we can safely assume *any play* from the opponents under this definition. In particular, if a certain move is projected to bring profit *P* assuming optimal play, it will bring at least *P* under any play from the opponents.

### The implementation

The algorithm uses Depth-First-Search with memoization to efficiently process the graph of all game evolution possibilities (game states or *subgames*). Clearly, the number of nodes in this graph differs from deal to deal, however, on average, it is in order of tens of millions. This can be reduced by roughly a factor of 10 by saving recursive calls on consecutive cards; e.g., it is unnecessary to consider both a queen of spades and a king of spades&mdash;the outcomes will be identical. In general, the algorithm takes anywhere from a few seconds to a few minutes to finish.


