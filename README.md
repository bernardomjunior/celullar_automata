# Celullar Automata Creation to simulate Cholera
- http://www.emro.who.int/health-topics/cholera-outbreak/index.html
- About modeling cholera: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4238032/

# How to run
- install python (and pip)
- install pandas: pip install pandas

# How to run it
- python main.py


# Modeling cholera rules
- Cholera is endemic or epidemic
- Once one's cured it is possible to be infectated again

# Configuration used on the first demonstration
- The choosen model was SIRS
- The cells keep in Infected state for 10 unities of time, in order to mimic the 10 dais infection duration
- The proximity function utilized considered all cells touching the one in question
- The cells keep in Recovered state for 2 unities of time
- The amount of infected neighbours need to infect cell is 4
