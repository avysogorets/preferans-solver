# Preferans (преферанс) solver.
## Introduction
Preferans is a popular Russian card game that gained its popularity in the early 19-th century. It is played with a French 32-card deck (7 to Ace) dealt for three hands of 10 cards each and a 2-card talon. In a nutshell, Preferans is a trick-taking game with the goal of fulfilling a declared contract, agreed upon by all players during the bidding stage. At this stage, players can bid to either (1) pass (2) play a game, or (3) play misere, leading to one of three types of contracts: (1) all-passes, (2) play, or (3) misere. All-passes occurs when all players pass and requires them to avoid taikng tricks, adding negative points for each trick taken. Let's talk about other contracts in more detail:
- *Play* is a contract where one "outstanding" player takes responsibility to take a declared number of tricks (no less than 6) under a major suit of his choice. The other players have an option to *whist*&mdash;contract themselves to take some or all of the remaining tricks. When exactly one player whists, he may choose to open up his and other player's cards (but not the *outstanding player's cards*), which is called "playing in the light". Ultimately, the outstanding player (and his opponents as a whole) are incentivized to take as many tricks as possible.
- *Misere* is a contract where one "outstanding" player obliges himself to take no tricks at all. The other two players open up their cards and try to force the other player to take as many tricks as possible. Note that misere is always played without a designated major suit. Misere is a rare and risky contract with a lot at stake and hence is not played too often.

The complete set of rules of Preferans is sophisticated and has a great deal of nuances; you can read more [here](https://en.wikipedia.org/wiki/Preferans).

## The task

This program is not a robot-player preconditioned to maximize returns, nor it is designed to produce optimal decisions for one of the players under incomplete information about the deal. Instead, it computes the outcome of the deal (the number of tricks taken by each player) assuming that *complete information* is available to all players (i.e., all cards open) and that they use it to *play optimally*. Optimal play is defined recursively: (1) it is optimal for a player with one card left to play it, and (2) it is optimal to play the card that leads to the most desirable outcome (according to the objective of the contract) assuming *optimal play* from the opponents. Note that we can safely assume *any play* from the opponents under this definition. In particular, if a certain move is projected to bring profit *P* assuming optimal play, it will bring at least *P* under any subsequent play from the opponents.

## Implementation

The algorithm uses Depth-First-Search with memoization to efficiently process the graph of all game evolution possibilities (game states or *subgames*). Clearly, the number of nodes in this graph differs from deal to deal, however, on average, it is in order of tens of millions. This can be reduced by roughly a factor of 10 by saving recursive calls on consecutive cards; e.g., it is unnecessary to consider both A&diams; and K&diams;&mdash;the outcomes will be identical. In general, the algorithm takes anywhere from a few seconds to a few minutes to finish.

## Example: Kovalevskaya's misere

For a quick demonstration, consider a well-known example&mdash;Kovalevskaya's misere. The deal is as follows:
- North: 7&spades; 8&spades; 9&spades; 10&spades; 8&clubs; 7&diams; 8&diams; 9&diams; 8&hearts; 9&hearts;
- East: K&spades; A&spades; 10&clubs; J&clubs; Q&clubs; A&diams; 10&hearts; Q&hearts; K&hearts; A&hearts; 
- South: J&spades; Q&spades; 7&clubs; 9&clubs; 10&diams; J&diams; Q&diams; K&diams; 7&hearts; J&hearts;

North is playing misere; South is to start (turns alternate clockwise). Can East and South catch it, i.e., force North to take one or more tricks? If so, how many under optimal play by North? The solution (in Russian) can be found [here](https://zen.yandex.ru/media/id/5b9e12e5b76d9000aa070845/reshenie-zadachi-s-mizerom-kovalevskoi-60cf77a8bb96047128248c10). Our solver will output the following:
```
Welcome to Preferans solver! Use S, C, D, H for spades, clubs, diamonds, and hearts, respectively.
Enter cards for hand #1 (format SUIT:KIND) separated by the space key: H:9 H:8 D:9 D:8 D:7 C:8 S:10 S:9 S:8 S:7
Enter cards for hand #2 (format SUIT:KIND) separated by the space key: S:K S:A C:10 C:J C:Q D:A H:10 H:Q H:K H:A
Enter cards for hand #3 (format SUIT:KIND) separated by the space key: S:J S:Q C:7 C:9 D:10 D:J D:Q D:K H:7 H:J
Indicate the game type (P for play or M for misere): M
Indicate the playing hand (1, 2, or 3): 1
Indicate the short hand (1, 2, or 3): 3
Copy that! Wait while the problem is being solved; this may take a few minutes...
------------------------ BEGIN SOLUTION ------------------------
[Game: MISERE]. Player 3 to start; major suit -.
Hand #1 [PLAY] H:9 H:8 D:9 D:8 D:7 C:8 S:10 S:9 S:8 S:7 (1)
Hand #2 [PASS] H:A H:K H:Q H:10 D:A C:Q C:J C:10 S:A S:K (3)
Hand #3 [PASS] H:J H:7 D:K D:Q D:J D:10 C:9 C:7 S:Q S:J (6)
[01] [3 D:10][1 D:7 ][2 D:A ] -> [0, 1, 0]
[02] [2 H:10][3 H:J ][1 H:8 ] -> [0, 1, 1]
[03] [3 D:J ][1 D:8 ][2 S:K ] -> [0, 1, 2]
[04] [3 D:Q ][1 D:9 ][2 S:A ] -> [0, 1, 3]
[05] [3 D:K ][1 S:7 ][2 H:Q ] -> [0, 1, 4]
[06] [3 S:J ][1 S:8 ][2 H:K ] -> [0, 1, 5]
[07] [3 S:Q ][1 S:9 ][2 H:A ] -> [0, 1, 6]
[08] [3 H:7 ][1 H:9 ][2 C:10] -> [1, 1, 6]
[09] [1 C:8 ][2 C:J ][3 C:9 ] -> [1, 2, 6]
[10] [2 C:Q ][3 C:7 ][1 S:10] -> [1, 3, 6]
Processed 20,236 subgames in 0 minute(s) 0 second(s).
```
The misere is caught! The best outcome for the North is to concede 1 trick.

## Limitations

While the solver tracks down optimal moves and prints them as part of the output, it can be difficult to undersatnd the logic behind them. In the above example, North plays spades in rounds 5,6 and 7, which may seem unreasonable at first, especially before we know that the misere is doomed. Hence, the solver provides only limited explanation for its projections.

Further, it is currently difficult to use the solver to guide play in a real game. First, it requires knowing all cards in all hands; this information is usually available only to the outstanding player and only when playing "in the light". Second, one's opponents may not play optimally&emdash;these scenarios are not memorized by the solver and cannot be retrieved without recomputing the current subgame from scratch. Finally, there are often many equally optimal solutions so that even if one's opponents play optimally, the same problem will likely come up. On the other hand, this solver can compute missing subgames almost instantly for their complexity decreases exponentially with the number of cards. Hence, provided a simple and fast way to encode subgames, it seems feasible to use this solver for optimal play in certain scenarios.

## Future work

There are a few directions to improve this solver; I will list them in order of increasing complexity:
 - Add support for all-passes "in the light" (although they are not played "in the light");
 - Attach an appropriate playing cards GUI for ease of visualization;
 - Design an efficient input-output pipeline to allow using the solver in real time in real games.
