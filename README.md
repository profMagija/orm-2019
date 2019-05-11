# Obrada rezultata merenja u Pajtonu

## step 1 - sakupljanje i priprema rezultata

Podatke sakupljajte u digitalnom formatu, kako kasnije ne biste morali da ih prekucavate - olakšaćete sebi muke i smanjiti mogućnost greške.
Najbolje koristite Excel (ili ekvivalent Excela) za unos.

### Pre obrade podataka:

Kao prvi red (zaglavlje kolone) stavite neku kratku, jedinstvenu oznaku koja je takođe validan identifikator za pajton:
- bez razmaka
- bez oznake jedinica

Podatke sačuvajte (Save As ...) u CSV format. Ovaj format je najlakši sa dalju obradu.

## step 2 - uvoženje podataka u Pajton

Biblioteka `pandas` ima gomilu funkcija koja omogućuju importovanje raznih vrsta fajlova. Ukoliko ste exportovali CSV fajl u prošlom koraku,
trebaće vam `pandas.read_csv` funkcija. Sve one vraćaju `DataFrame` objekat (tabelu):

```py
podaci = pandas.read_csv("putanja/do/fajla.csv")
```

Nakon toga, pojedinačnim kolonama se pristupa na jedan od sledećih načina:
- `podaci.ime_kolone`
- `podaci['ime_kolone']`

## step 3 - računanje sa podacima

Sve kolone se ponašaju slično kao numpy array objekti, dakle sve operacije se obavljaju elemen-wise (element po element). 
To nam omogućava da sa podacima operišemo na intuitivan način:

```py
# ovo će savrati svaki element X sa svakim elementom Y
z = podaci.x + podaci.y

# ovo će vratiti niz logaritama elemenata Z
w = np.log(z)
```

### računanje grešaka

U primeru je data funkcija `majoriraj` koja majorira date **NENEGATIVNE** argumente po pravilima za majoriranje argumenata. U nastavku su dati neki primeri izvedenih veličina i kako se računaju njihove vrednosti i greške.

- Z = X + Y

  ```py
  z = x + y

  # greška:
  delta_z = majoriraj( delta_x + delta_y )
  ```

- Z = X Y

  ```py
  z = x * y

  # greška:
  delta_z = majoriraj( (delta_x/x + delta_y/y) * z )
  # ili (ukoliko već imamo relativne greške za X i Y)
  rel_z = rel_x + rel_y
  delta_z = majoriraj( rel_z * z )
  ```

- Z = ln X

  ```py
  z = np.log(x)

  # greška:
  delta_z = majoriraj( delta_x / x )
  ```



## step 4 - crtanje grafika

Biblioteka `matplotlib.pyplot`, obično importovana kao `plt`

### `plt.plot(x, y, format, ...)` - obično crtanje grafika

- za `x` se podrazumeva `[0, 1, 2, ...]`
  - dakle `plt.plot(y)` je isto što i `plt.plot([0, 1, ...], y)`
  - obično ćete hteti da za svaki slučaj tačno navedete x-koordinate
- za tačke stavite `'.'` kao format

### `plt.errorbar(x, y, y_err, x_err, format, ...)` - crtanje grafika sa greškama

- pazite na redosled argumenata

### `plt.title('Naslov Grafika')` - dodavanje naslova grafika

### `plt.xlabel('x opis')`, `plt.ylabel('y opis')` - labele za ose na grafiku

### `plt.show()` - prikazuje grafik

- takođe briše grafik nakon što ga prikaže. Sve naredne `plt` komande crtaju novi plot.

### `plt.savefig('putanja/do/fajla.png')` - čuva plot u fajl

- najbolje pozovite pre svakog `plt.show()` kako ne biste ručno čuvali svaki put.

## step 5 - linearni fit

Ako su nam dati podaci o zavisnosti X i Y linearni fit tih podataka se može napraviti.

```py
k, n = np.polyfit(X, Y, 1)

# k - koeficijent pravca
# n - odsečak na y-osi
```

Konstanta 1 govori da je u pitanju linearni fit (`np.polyfit` može da radi polinomni fit proizvoljnog stepena) 
