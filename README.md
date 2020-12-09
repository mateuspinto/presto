# PRESTO

PRESTO is a simulator for scheduling processes and physical memory made in Python 3, with a design highly inspired by htop.



## How to run

    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python src/Main.py

## Suported process schedulers

 - FIFO
 - Lottery
 - Multiple Queues
 - Orwell Lottery
 - Priority
 - Round Robin
 - Shortest Job First
 - Shortestest remaining time next
 
## Suported memory schedulers
 - Best fit
 - Worst fit
 - First fit
 - Next fit

## References
Todos os algoritmos foram baseados no livro "Sistemas operacionais modernos - Tanenbaum".
