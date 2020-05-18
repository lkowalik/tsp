# Co to jest?
Skrypt `tsp.py` znajdujący optymalną trasę komiwojażera dla 51 miast w Polsce, na potrzeby artykułu w miesięczniku Delta

# Wymagania

1. Python (https://www.python.org/downloads/)
2. Biblioteka [matplotlib](https://matplotlib.org/) do wizualizacji. Instalacja: `pip install matplotlib`
3. Biblioteka [pulp](https://pypi.org/project/PuLP/) do rozwiązywania programów liniowych. Instalacja: `pip install pulp`
4. Biblioteka [basemap](https://matplotlib.org/basemap/) do rzutowania współrzędnych geograficznych 

   Instalacja Windows: 
   1. ściągnąć plik xxx.whl ze strony https://www.lfd.uci.edu/~gohlke/pythonlibs/#basemap
   2. `pip install [xxx.whl]`
   
   Instalacja Linux:
   ```
   sudo apt-get update
   sudo apt-get install libgeos-dev
   sudo apt-get install python-mpltoolkits.basemap
   ```
  
