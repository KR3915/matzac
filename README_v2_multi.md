# Multiplayer Space Invaders v2.0 Multi-Shot Edition

## 🆕 Nové funkce
- **Více střel najednou**: Můžete střílet až 5 střel současně (multiplayer) / 10 střel (singleplayer)
- **Singleplayer testovací verze**: Pro testování střel bez síťové komunikace
- **Vylepšená střelba**: Střely se neblokují navzájem

## 📁 Soubory

### Multiplayer verze:
- **`host_v2_multi.py`** - Server s podporou více střel
- **`client_v2_multi.py`** - Klient s podporou více střel

### Singleplayer testovací verze:
- **`singleplayer_test.py`** - Pro testování střel bez sítě

## 🎮 Herní mechanika

### Multiplayer
- **Host** (zelený) hraje v dolní části obrazovky (y=18)
- **Klient** (červený) hraje v horní části obrazovky (y=1)
- **Nepřátelé** (oranžoví) se pohybují v horní části obrazovky
- **Střely** (žluté) se pohybují vertikálně
- **Maximálně 5 střel najednou** pro každého hráče

### Singleplayer
- **Hráč** (zelený) hraje v dolní části obrazovky (y=18)
- **Nepřátelé** (oranžoví) se pohybují v horní části obrazovky
- **Střely** (žluté) se pohybují nahoru
- **Maximálně 10 střel najednou**

## 🚀 Instalace a spuštění

### 1. Singleplayer test (doporučeno pro testování)
1. Nahrajte `singleplayer_test.py` na Micro:bit
2. Spusťte kód - žádná síťová konfigurace není potřeba
3. Testujte střelbu!

### 2. Multiplayer verze
1. **Host**: Nahrajte `host_v2_multi.py` na první Micro:bit
2. **Klient**: Nahrajte `client_v2_multi.py` na druhý Micro:bit
3. Upravte `SERVER_IP` v klientovi na IP adresu hosta
4. Spusťte oba kódy

## 🎯 Ovládání

### Singleplayer
- **Tlačítko A + vlevo**: Pohyb doleva
- **Tlačítko A + vpravo**: Pohyb doprava
- **Tlačítko A + Enter**: Střelba (můžete střílet opakovaně)

### Multiplayer
- **Host**: Stejné ovládání jako singleplayer
- **Klient**: Stejné ovládání jako singleplayer

## 🎨 Herní prvky

### Barvy
- **Zelená**: Hráč/Host (dole)
- **Červená**: Klient (nahoře) - pouze multiplayer
- **Oranžová**: Nepřátelé
- **Žlutá**: Střely

### Skóre
- 10 bodů za každého zničeného nepřítele
- Zobrazuje se na konci hry

### Konec hry
- **Singleplayer**: Zelená obrazovka + blikající skóre
- **Multiplayer**: 
  - Zelená obrazovka: Klient vyhrál
  - Červená obrazovka: Host vyhrál
  - Žlutá obrazovka: Remíza
  - Oranžová obrazovka: Nepřátelé vyhráli

## 🔧 Technické detaily

### Singleplayer
- **Herní plocha**: 10x20 pixelů
- **FPS**: 10
- **Max střel**: 10 najednou
- **Žádná síťová komunikace**

### Multiplayer
- **Herní plocha**: 10x20 pixelů
- **FPS**: 10
- **Max střel**: 5 najednou pro každého hráče
- **Komunikace**: JSON přes TCP socket
- **Timeout**: 5 sekund

## 🎯 Výhody nové verze

1. **Rychlejší střelba**: Můžete střílet opakovaně bez čekání
2. **Taktické možnosti**: Více střel = více možností
3. **Lepší gameplay**: Dynamičtější hra
4. **Testování**: Singleplayer verze pro snadné testování

## 🐛 Řešení problémů

### Singleplayer nefunguje
- Zkontrolujte, zda je kód správně nahrán
- Restartujte Micro:bit

### Multiplayer problémy
- Nejdříve otestujte singleplayer verzi
- Zkontrolujte Wi-Fi připojení
- Ověřte IP adresu serveru

### Střely se nezobrazují
- Zkontrolujte, zda stisknete A+Enter
- Můžete střílet až MAX_SHOTS střel najednou

## 🎮 Tipy pro hru

1. **Rychlá střelba**: Stiskněte A+Enter opakovaně pro rychlou střelbu
2. **Taktické střílení**: Použijte více střel pro pokrytí větší oblasti
3. **Pohyb**: Pohybujte se při střelbě pro lepší úhybnost
4. **Cílení**: Zaměřte se na nepřátele v různých pozicích

## 🔄 Rozšíření

- Přidání různých typů střel
- Power-upy pro více střel
- Různé rychlosti střel
- Animace střel
- Zvukové efekty
