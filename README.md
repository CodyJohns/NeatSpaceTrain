## Playing Space Train with NEAT genetic machine learning algorithm

Uses pygame and neat-python packages

#### Inputs (20 so far)

1) Train X position*
2) Train Y position*
3) Is currently shooting
4) Mouse position X*
5) Mouse position Y*
6) inputs 6 to 20 are a flattened, concatenated array of up to 3 enemies with:
a) Enemy position X*
b) Enemy position Y*
c) Enemy velocity*
d) Enemy relative distance X*
e) Enemy relative distance Y*

*these values have been normalized according to screen dimensions

#### Outputs (5)

1) Move left
2) Move right
3) Shoot
4) Move mouse X
5) Move mouse Y

### Analysis

These are some observations of 5 models that were trained. The only differences in training sessions were:
1) changing the not-moving fitness deduction to see if genomes with higher penalties for not moving enough would eliminated.
2) changing the fitness deduction when the genome was considered not moving because it was already at the screen limits. Because of the above the models would continue to press left or right to keep "moving" in order to not be penalized. So instead we check if the train is still at the same x coordinate to check for moving and if not we penalize the genome.
3) the final calculation of the fitness value for a genome. I first added to the fitness value the final score minus the amount of time and shots each genome took. However, it turned out to do better when I resorted to the final score * 100 minus and a bonus if it reached the score threshold as quickly as possible.

Even with these changes, the models didn't seem to improve after about 200 epochs. However, the models learned to aim and shoot when a ship was nearby. I would find occasionally that because the models didn't move around enough that the models would continue shooting at the last ship on the screen, but not updating the mouse aim so the last ship would slip by the bullets. The model did move the train to the right proving that it does know how to move. If you think about it the game is simulating the train moving through space at a high rate of speed and the ships from a speed perspective move slower when moving right. The models appear to have learned this and therefore move all the way to the right of the screen in order to have more time to shoot the enemy ships. As for the lack of movement it appears that the models would rather be penalized by not moving after being all the way to right in order to rack up the score by shooting down enemies.

Overall, the models do a good job aiming and shooting down enemies. I would have liked it if the models learned to move around, but according to evolution it always finds a way to be efficient.

