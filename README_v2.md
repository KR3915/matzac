# Multiplayer Space Invaders v2.0 pro Micro:bit

## Popis
Multiplayer hra Space Invaders pro dva hráče na mikrobitech s herní plochou 10x20 pixelů.

## Herní mechanika
- **Host** (zelený) hraje v dolní části obrazovky (y=18)
- **Klient** (červený) hraje v horní části obrazovky (y=1)
- **Nepřátelé** (oranžoví) se pohybují v horní části obrazovky
- **Střely** (žluté) se pohybují vertikálně
- Hráči mohou střílet na nepřátele i na sebe navzájem
- Hra končí, když jsou všichni nepřátelé zničeni nebo oba hráči zemřou

## Instalace a spuštění

### 1. Host (Server)
1. Nahrajte `host_v2.py` na první Micro:bit
2. Spusťte kód - vytvoří se Wi-Fi hotspot "ESP-AP"
3. Poznamenejte si IP adresu serveru (vypíše se v konzoli)

### 2. Klient
1. Nahrajte `client_v2.py` na druhý Micro:bit
2. Upravte `SERVER_IP` v kódu na IP adresu hosta
3. Spusťte kód - připojí se k hostovi

## Ovládání

### Host (zelený hráč)
- **Tlačítko A + vlevo**: Pohyb doleva
- **Tlačítko A + vpravo**: Pohyb doprava
- **Tlačítko A + Enter**: Střelba

### Klient (červený hráč)
- **Tlačítko A + vlevo**: Pohyb doleva
- **Tlačítko A + vpravo**: Pohyb doprava
- **Tlačítko A + Enter**: Střelba

## Herní prvky

### Barvy
- **Zelená**: Host (dole)
- **Červená**: Klient (nahoře)
- **Oranžová**: Nepřátelé
- **Žlutá**: Střely

### Skóre
- 10 bodů za každého zničeného nepřítele
- Hráč s vyšším skóre vyhrává při zničení všech nepřátel

### Konec hry
- **Zelená obrazovka**: Klient vyhrál
- **Červená obrazovka**: Host vyhrál
- **Žlutá obrazovka**: Remíza
- **Oranžová obrazovka**: Nepřátelé vyhráli

## Síťová konfigurace
- **SSID**: ESP-AP
- **Heslo**: protabulesa
- **Port**: 1234
- **Protokol**: TCP

## Technické detaily
- **Herní plocha**: 10x20 pixelů
- **FPS**: 10
- **Komunikace**: JSON přes TCP socket
- **Timeout**: 5 sekund

## Řešení problémů

### Klient se nemůže připojit
1. Zkontrolujte, zda je host spuštěný
2. Ověřte IP adresu serveru
3. Zkontrolujte Wi-Fi heslo

### Hra laguje
1. Zkontrolujte síťové připojení
2. Snižte FPS v kódu
3. Zkraťte timeout hodnoty

### Chyby v komunikaci
1. Restartujte oba mikrobity
2. Zkontrolujte JSON formát dat
3. Ověřte síťovou konfiguraci

## Rozšíření
- Přidání více typů nepřátel
- Power-upy a speciální zbraně
- Různé úrovně obtížnosti
- Zvukové efekty
- Animace
