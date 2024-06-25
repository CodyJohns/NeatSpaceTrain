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