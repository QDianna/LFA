# LFA – Etapa 2: Regex → NFA (Thompson)

## Descriere
Implementare în Python a algoritmului **Thompson** pentru a construi un **NFA** echivalent cu un regex dat.  
Regex-urile suportă operatori de bază și extensii.

## Funcționalități
- Clasa `Regex` cu metoda `thompson()` → returnează un `NFA`
- Operatori: concatenare implicită, `|`, `*`, `+`, `?`
- Sugars: `[a-z]`, `[A-Z]`, `[0-9]`
- Suport pentru `eps` și caractere escape.

## Cum rulezi
1. Parsează regex-ul cu `parse_regex("a(b|c)*")`.  
2. Construiește NFA cu `regex.thompson()`.  
3. Testează recunoașterea prin conversia ulterioară la DFA (subset construction).
