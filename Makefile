# =========================
# IN520 - Regexp Equality
# =========================

# Dossiers
SRC_DIR = src
TESTS_DIR = tests
GEN_DIR = generated

# Test du lexer
test_regexp_lex:
	cd $(SRC_DIR) && flex -o ../$(GEN_DIR)/lex.yy.c regexp.l
	gcc -I$(SRC_DIR) -o $(TESTS_DIR)/test_lexer $(TESTS_DIR)/test_lexer.c $(GEN_DIR)/lex.yy.c -lfl
	cd $(TESTS_DIR) && ./test_lexer < test_lexer.txt

# Test lex + yacc ensemble : génère main.py depuis test.1 puis exécute python
test_regexp_yacc:
	cd $(SRC_DIR) && bison -d -o ../$(GEN_DIR)/regexp.tab.c regexp.y
	cd $(SRC_DIR) && flex -o ../$(GEN_DIR)/lex.yy.c regexp.l
	gcc -I$(GEN_DIR) -I$(SRC_DIR) -o $(GEN_DIR)/regexp $(GEN_DIR)/regexp.tab.c $(GEN_DIR)/lex.yy.c -lfl
	$(GEN_DIR)/regexp < $(TESTS_DIR)/test.1 > $(GEN_DIR)/main.py
	PYTHONPATH=$(SRC_DIR) python3 $(GEN_DIR)/main.py

# Test de l'automate
test_automate:
	PYTHONPATH=.:$(SRC_DIR) python3 $(TESTS_DIR)/test_automate.py

# Nettoyage - supprime tous les fichiers générés
clean:
	rm -f $(GEN_DIR)/lex.yy.c \
	      $(GEN_DIR)/regexp.tab.c \
	      $(GEN_DIR)/regexp.tab.h \
	      $(GEN_DIR)/regexp \
	      $(GEN_DIR)/main.py \
	      $(TESTS_DIR)/test_lexer
	rm -rf $(SRC_DIR)/__pycache__ $(TESTS_DIR)/__pycache__
	rm -f *.pyc
	# S'assure que le dossier generated existe toujours
	mkdir -p $(GEN_DIR)

# Aide
help:
	@echo "Commandes disponibles:"
	@echo "  make test_regexp_lex    - Teste uniquement le lexer"
	@echo "  make test_regexp_yacc   - Teste lexer + parser (génère main.py)"
	@echo "  make test_automate      - Teste les fonctions d'automate Python"
	@echo "  make clean             - Nettoie tous les fichiers générés"
	@echo "  make help              - Affiche cette aide"

.PHONY: test_regexp_lex test_regexp_yacc test_automate clean help