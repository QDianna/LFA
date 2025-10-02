# LFA – Etapa 1: NFA → DFA (Subset Construction)

## Descriere
Implementare în Python a conversiei unui **NFA** într-un **DFA** folosind algoritmul Subset Construction.  
Se verifică acceptarea unui cuvânt de către DFA-ul rezultat.

## Funcționalități
- Clasa `NFA`: 
  - `epsilon_closure(state)`
  - `subset_construction()` → returnează DFA
- Clasa `DFA`: 
  - `accept(word)` → True/False
- Stările DFA sunt reprezentate ca `frozenset` de stări NFA.

## Cum rulezi
1. Rulează implementarea pentru a construi DFA dintr-un NFA dat.  
2. Folosește `dfa.accept("cuvant")` pentru a verifica apartenența la limbaj.
