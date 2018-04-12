# SeriesWatch
Projekt eszközök beadandó

## Telepítés / Használat
Telepítsd fel a Python 3-at: https://www.python.org/downloads/

A verziót telepítés után így tudod ellenőrizni:
```
python --version
```
Nyiss egy parancssort/terminált, telepítsd a Django-t és ellenőrizd a verziót (ez opcionális): 
```
pip install django
python -m django --version
```
Ahhoz, hogy működjenek a lekérdezések, mielőtt elindítod a szervert, hozz létre a főkönyvtárba egy
**conf.cnf** fájlt a **conf_example.cnf** mintájára és ebben add meg az api_key-t


Hozd létre az adatbázis és a szükséges adattáblákat a következő parancsokkal:
```
python manage.py makemigrations
python manage.py migrate
```
Így tudsz létrehozni admin fiókot:
```
python manage.py createsuperuser
```
_(Teszt fiók létrehozása lejebb)_

A projekt főkönyvtárában (SeriesWatch) a következő paranccsal tudod elindítani a szervert:
```
python manage.py runserver
```
Valami ehhez hasonlót fogsz látni, ha mindent jól csináltál:
```
Performing system checks...

System check identified no issues (0 silenced).

You have unapplied migrations; your app may not work properly until they are applied.
Run 'python manage.py migrate' to apply them.

March 22, 2018 - 15:50:53
Django version 2.0, using settings 'mysite.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

A böngésződből itt fogod elérni: http://127.0.0.1:8000/


Ez után a http://127.0.0.1:8000/admin felületen a létrehozott fiókkal bejelentkezve a Users táblában tudsz létrehozni teszt fiókokat.


---

Design most már elérhető az index.html-en keresztül, egyelőre nem túl jól működik.
