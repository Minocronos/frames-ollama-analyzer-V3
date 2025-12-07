# POURQUOI ON NE FAIT PAS TOUT LE TEMPS DE L'INJECTION ?

C'est une excellente question. Si c'est si génial, pourquoi on ne code pas **tout** comme ça ?

La réponse courte : **Parce que c'est lourd.**

---

## 1. L'EXEMPLE DE L'USINE À GAZ (Overkill)

Imagine tu veux juste afficher "Bonjour".

### 👉 Sans Injection (Simple, efficace)
```python
print("Bonjour !")
```
*3 secondes à écrire, 0 prise de tête.*

### 👉 Avec Injection (L'enfer pour rien)
```python
class AfficheurDeMessage:
    def afficher(self, texte):
        print(texte)

class ApplicationBonjour:
    def __init__(self, service_affichage):
        self.service = service_affichage
    
    def run(self):
        self.service.afficher("Bonjour !")

# Configuration (Wiring)
mon_afficheur = AfficheurDeMessage()
app = ApplicationBonjour(mon_afficheur)
app.run()
```
*Tu as écrit 15 lignes pour faire un `print`. C'est ridicule pour un script simple.*

---

## 2. LA "MAGIE" DE PYTHON (Monkeypatching)

En Java ou C#, l'injection est OBLIGATOIRE pour tester, car le code est "verrouillé".
Mais Python est **dynamique**. On peut tricher.

Même si tu as codé "mal" (sans injection), Python te permet de remplacer des morceaux de code à la volée pendant les tests.

```python
# Ton code "mal fait" (couplage fort)
import time
def attendre():
    time.sleep(10) # Bloque 10 secondes !

# Ton test (Python permet de remplacer time.sleep !)
def test_rapide(monkeypatch):
    monkeypatch.setattr(time, 'sleep', lambda x: None) # Hop, on désactive le sleep
    attendre() # Ça prend 0 seconde !
```

C'est pour ça que beaucoup de développeurs Python se disent : *"Bof, pas besoin d'injection, je bidouillerai mes tests avec `mock` ou `monkeypatch`."*

---

## 3. ALORS, QUAND L'UTILISER ?

Il y a une ligne rouge à franchir.

### ✅ NE L'UTILISE PAS SI :
*   Tu fais un script simple (ex: `setup.bat`, petit script de data science).
*   Ton projet fait moins de 5-10 fichiers.
*   Tu es le seul à bosser dessus et tu veux aller vite.

### 🚀 UTILISE-LE SI :
*   **Ton projet grossit** : Tu as 50+ fichiers, des modules partout.
*   **Tu utilises un Framework** : FastAPI, Django, NestJS (ils te forcent un peu à le faire, et c'est tant mieux).
*   **Tu veux changer de "briques" souvent** : Exemple : passer de SQLite à PostgreSQL, ou de OpenAI à Claude, sans réécrire tout ton code.

## RÉSUMÉ

L'injection, c'est comme ranger ses outils dans des boîtes étiquetées.
*   Pour bricoler un cadre photo, c'est chiant, tu veux juste ton marteau tout de suite.
*   Pour construire une maison, c'est **indispensable**, sinon c'est le chaos.
