# Simulation

## Can we simulate one-on-one battles?

### The first pass

As a very basic way to play, kids sometimes will just battle Pokemon one on one, without worrying about energies, trainers, etc. Can we randomly pit two Pokémon cards against each other?

In [simulator.py](../game/simulator.py), we randomly select two Pokémon cards, simulate a battle against the two cards where attacks are chosen at random. We run 100 battles like this and calculate which Pokémon wins the most battles. 

Note that this is not a realistic game scenario, but it is a stepping stone to more complex game simulation. 

You can run the simulator on the command line.

I also built a simple tournament script: [tournament.py](../game/tournament.py). This script pits all of the Pokémon in the database in a tournament. 

So, who is the winner? I've only run this a few times, and the winner appears to be:
Mega Charizard EX. Even though I've run this a handful of times, the winner is the Mega Charizard EX either from the Flashfire or Evolutions expansion sets.

### The next step

For the next version of this one-on-one battle simulation, instead of randomly choosing an attack, I will add in attaching energies and determining which attack is possible given the attached energies.