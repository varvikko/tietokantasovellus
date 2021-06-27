https://tsohachan.herokuapp.com/

# Kuvafoorumi

## Käyttö

Kyseessä on keskustelufoorumi, jossa viesteihin voi lisäksi liittää kuvan, eli ns. kuvafoorumi. Foorumia voi katsella ja viestejä voi lähettää kuka tahansa anonyymisti. Lisäksi foorumiin voi luoda oman tunnuksen. Foorumilla on erilaisia keskustelualueita. Jokainen lanka (ketju) ja viesti kuuluu jollekin alueelle.

Jokaiselle foorumille vierailevalle luodaan automaattisesti tunnus. Näin foorumin käyttö onnistuu myös ilman rekisteröintiä. Luomalla tunnuksen voi kuitenkin määritellä haluamansa käyttäjätunnuksen ja salasanan. Anonyymit käyttäjät tunnistetaan cookien talletettavan id:n perusteella, joten ne häviävät mikäli mikäli evästeet tyhjennetään. Rekisteröidylle tunnukselle voi kirjautua aina.

Omia viestejä ja ketjuja voi poistaa ja muokata. Muiden luomiin viesteihin ja ketjuhin voi vastava ja niitä voi piilottaa. Toisiin viesteihin voi vastata liittämällä omaan viestiin ko. viestin id:n. Käyttäjä voi myös hakea viestejä tietyn hakusanan perusteella.

Jokaisella alueella on oma näkymänsä, jossa näkyvät ketjut joihin on viimeisimpänä vastattu. Lisäksi etusivulla näkyvät jokaisen alueen suosituimmat ketjut.

Ylläpitäjä voi poistaa minkä tahansa ketjun tai viestin. Lisäksi ylläpitäjä voi asettaa käyttäjälle eston.

# Sovelluksen tila

Sovellukseen on nyt totetutettu kaikki em. toiminnot.

# Deployment

## Local deployment

Run

```sh
docker-compose up --build
```

App will open on port 5000

