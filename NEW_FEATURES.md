# Nové Funkce - Matzac Game

## 🎮 Přehled Nových Funkcí

Hra byla výrazně vylepšena s novými mechanikami pro lepší gameplay a strategii.

## 🚀 Hlavní Novinky

### 1. **Zpomalený Pohyb Hráče**

#### Problém
- Hráč se pohyboval příliš rychle
- Obtížná kontrola během střelby
- Nemožnost přesného manévrování

#### Řešení
```python
# Cooldown systém pro pohyb
player_move_cooldown = 0
player_move_delay = 3  # frames between moves

def hrac1_do_leva():
    if player_move_cooldown <= 0:
        # pohyb...
        player_move_cooldown = player_move_delay
```

#### Výhody
- **Lepší kontrola**: Hráč má čas na reakci
- **Přesnější manévrování**: Možnost vyhnout se střelám
- **Strategičtější gameplay**: Plánování pohybů

### 2. **Systém Více Střel**

#### Problém
- Pouze jedna střela na obrazovce
- Omezená palebná síla
- Nemožnost pokrýt větší oblast

#### Řešení
```python
# Systém více střel
active_shots = []  # List of active shots
max_shots = 3      # Maximum number of shots on screen
shot_cooldown = 0
shot_delay = 10    # frames between shots

class Shot:
    def __init__(self, x, y, owner="player"):
        self.x = x
        self.y = y
        self.owner = owner
        self.active = True
```

#### Výhody
- **Více střel**: Až 3 střely současně
- **Lepší pokrytí**: Možnost střílet do více směrů
- **Strategické střelba**: Kombinace střel pro maximální efekt

### 3. **Předělané Buffy**

#### Nové Typy Buffů

##### **1. Big Shot (Fialová)**
- **Efekt**: 3x3 pattern střel
- **Trvání**: 200 snímků (~10 sekund)
- **Použití**: Automaticky při střelbě

##### **2. Clone (Tyrkysová)**
- **Efekt**: Vytvoří klona, který střílí
- **Trvání**: 300 snímků (~15 sekund)
- **Použití**: Automaticky při aktivaci

##### **3. Slow Enemy (Modrá)**
- **Efekt**: Nepřátelé se pohybují 3x pomaleji
- **Trvání**: 250 snímků (~12.5 sekund)
- **Použití**: Automaticky při aktivaci

##### **4. Rapid Fire (Žlutá) - NOVÝ**
- **Efekt**: 3x rychlejší střelba
- **Trvání**: 150 snímků (~7.5 sekund)
- **Použití**: Automaticky při aktivaci

#### Vylepšení Buffů
- **Delší trvání**: Všechny buffy trvají déle
- **Lepší vizualizace**: Jasné barvy pro každý typ
- **Vyváženost**: Všechny buffy jsou užitečné

## 🔧 Technické Detaily

### Pohybový Systém
```python
# Cooldown pro pohyb
if player_move_cooldown <= 0:
    # povol pohyb
    player_move_cooldown = player_move_delay
```

### Střelící Systém
```python
# Vytvoření střely
def create_shot(x, y, owner="player"):
    if len(active_shots) < max_shots:
        new_shot = Shot(x, y, owner)
        active_shots.append(new_shot)
        return True
    return False

# Aktualizace střel
def update_shots():
    for shot in active_shots:
        shot.y -= 1  # Pohyb nahoru
        # Kontrola kolizí...
```

### Buff Systém
```python
# Nový buff - Rapid Fire
elif buff_type == "rapid_fire":
    rapid_fire_active = True
    rapid_fire_timer = rapid_fire_duration
    print("Rapid fire activated!")

# Vylepšené trvání
buff_duration = 200      # Big Shot
clone_duration = 300     # Clone
enemy_slow_duration = 250 # Slow Enemy
rapid_fire_duration = 150 # Rapid Fire
```

## 🎯 Herní Výhody

### **Pro Hráče**
- **Lepší kontrola**: Zpomalený pohyb umožňuje přesnost
- **Více možností**: Systém více střel dává více taktik
- **Strategické buffy**: Každý buff má jasné využití
- **Delší trvání**: Buffy vydrží dostatečně dlouho

### **Pro Gameplay**
- **Vyváženost**: Všechny mechaniky jsou užitečné
- **Strategie**: Kombinace buffů pro maximální efekt
- **Obtížnost**: Hra je náročnější ale spravedlivá
- **Zábava**: Více možností pro kreativní hraní

## 🎮 Ovládání

### **Pohyb**
- **A-Left/A-Right**: Pohyb s cooldownem (3 snímky)
- **Přesnější kontrola** pro vyhýbání se střelám

### **Střelba**
- **A-Enter**: Střelba s cooldownem (10 snímků)
- **Až 3 střely** současně na obrazovce
- **Rapid Fire**: 3x rychlejší střelba

### **Buffy**
- **Automatické sbírání**: Dotyk s buffem
- **Manuální aktivace**: B-Down
- **Vizualizace**: Jasné barvy pro každý typ

## 📊 Výkonnostní Metriky

### **Před Vylepšením**
- **Pohyb**: Příliš rychlý
- **Střely**: 1 střela najednou
- **Buffy**: Krátké trvání
- **Strategie**: Omezené možnosti

### **Po Vylepšení**
- **Pohyb**: Kontrolovaný s cooldownem
- **Střely**: Až 3 střely současně
- **Buffy**: Delší trvání, více typů
- **Strategie**: Mnoho kombinací

## 🎯 Doporučení pro Hraní

1. **Používejte cooldown**: Plánujte pohyby dopředu
2. **Kombinujte střely**: Využijte více střel pro pokrytí
3. **Prioritizujte buffy**: Každý buff má své využití
4. **Experimentujte**: Zkuste různé kombinace buffů
5. **Trénujte timing**: Naučte se načasování střel

Hra je nyní mnohem strategičtější a zábavnější s těmito novými mechanikami!
