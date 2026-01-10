# 🧠 IN520 – Test d’égalité de langages rationnels

Projet de Théorie des Langages – L3 Informatique UVSQ  
Vérification de l’égalité de deux expressions rationnelles par construction d’automates finis.

---

## 🎯 Objectif

Ce projet permet de déterminer si **deux expressions rationnelles** représentent **le même langage**.

Le programme :
1. Lit un fichier contenant **deux regex**
2. Construit leurs automates finis
3. Les déterminise, complète et minimise
4. Compare leurs langages
5. Affiche :

EGAL  
ou  
NON EGAL

---

## 📁 Structure du projet

.
├── src/  
│   ├── regexp.l        # Analyseur lexical (Flex)  
│   ├── regexp.y        # Analyseur syntaxique (Yacc/Bison)  
│   ├── automate.py    # Bibliothèque d'automates  
│   └── runner.sh      # Script de compilation/exécution  
│  
├── tests/  
│   └── test.1         # Fichier contenant 2 expressions  
│  
├── generated/  
│   └── main.py        # Programme Python généré automatiquement  
│  
├── Makefile  
└── README.md  

---

## 📥 Format du fichier d’entrée

Un fichier texte contenant **exactement deux lignes**, chacune représentant une expression rationnelle :

(a+b)*.a  
(a+b)*.a  

---

## ⚙️ Fonctionnement

### 1. Analyse lexicale & syntaxique

- `regexp.l` découpe les symboles lexicaux  
- `regexp.y` construit du **code Python**  
- Ce code est généré dans `generated/main.py`

---

### 2. Construction des automates

Chaque expression est transformée en automate, puis :
- déterminisée  
- complétée  
- minimisée  

---

### 3. Comparaison

Les automates minimisés sont comparés :
- Identiques → EGAL  
- Différents → NON EGAL  

---

## ▶️ Exécution

Sous Linux / WSL :

chmod +x src/runner.sh  
./src/runner.sh tests/test.1  

---

## 🧑‍🤝‍🧑 Travail en binôme

| Branche Git | Rôle |
|------------|-----|
| feature/parser-yacc | Analyse lexicale et syntaxique |
| feature/automate-ops | Opérations sur automates |

---

## 📚 Technologies

- Python 3  
- Flex  
- Bison (Yacc)  
- GitHub  

---

## 👨‍🎓 Projet académique

Projet réalisé dans le cadre du module **IN520 – Théorie des Langages**  
Université de Versailles Saint-Quentin-en-Yvelines (2025–2026)
