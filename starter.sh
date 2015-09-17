#!/bin/bash

python main.py --number=3 --data=EURUSD.hst --layers=20 --prediction=2 > 3.20.txt &
python main.py --number=3 --data=EURUSD.hst --layers=10 --prediction=2 > 3.10.txt &
python main.py --number=3 --data=EURUSD.hst --layers=50 --prediction=2 > 3.50.txt &
python main.py --number=10 --data=EURUSD.hst --layers=50 --prediction=2 > 10.50.txt &
python main.py --number=10 --data=EURUSD.hst --layers=100 --prediction=2 > 10.100.txt &
python main.py --number=10 --data=EURUSD.hst --layers=25 --prediction=2 > 10.25.txt &
python main.py --number=50 --data=EURUSD.hst --layers=250 --prediction=2 > 50.250.txt &
python main.py --number=50 --data=EURUSD.hst --layers=100 --prediction=2 > 50.100.txt &