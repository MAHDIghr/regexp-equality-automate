%{
#include <stdio.h>
#include <stdlib.h>

/* yylex vient de regexp.l */
int yylex(void);
void yyerror(const char *s);

/* Compteur global pour nommer a0, a1, a2, ... */
static int state_count = 0;
%}

/* Valeurs associées aux tokens/non-terminaux */
%union {
    char c;
    int  state_id;
}

/* Tokens (DOIVENT matcher regexp.l) */
%token <c> LETTRE
%token EPS
%token PLUS POINT ETOILE PAR_G PAR_D FIN_LIGNE INCONNU

/* Types des non-terminaux (on remonte un id d'automate a<id>) */
%type <state_id> E concat repeat atom

/* Précédences :
   - ETOILE est postfix, plus prioritaire
   - concat (POINT et concat implicite) au milieu
   - PLUS le moins prioritaire
*/
%left PLUS
%left POINT
%left ETOILE

%%

/* Programme = 2 lignes d'expressions régulières */
input:
      {
        /* Entête Python */
        printf("from automate import *\n");
      }
      expr_un expr_deux
    ;

/* Première expression sur une ligne */
expr_un:
      E FIN_LIGNE
      {
        int m = state_count++;
        printf("a%d = tout_faire(a%d)\n", m, $1);
        printf("res1 = a%d\n", m);
      }
    ;

/* Deuxième expression sur une ligne + comparaison */
expr_deux:
      E optional_newline
      {
        int m = state_count++;
        printf("a%d = tout_faire(a%d)\n", m, $1);
        printf("res2 = a%d\n", m);

        printf("if egal(res1, res2):\n");
        printf("    print(\"EGAL\")\n");
        printf("else:\n");
        printf("    print(\"NON EGAL\")\n");
        exit(0);
      }
    ;
    
optional_newline:
      FIN_LIGNE
    | /* vide */
    ;

/* Expression avec + (union), associatif gauche */
E:
      E PLUS concat
      {
        $$ = state_count++;
        printf("a%d = union(a%d, a%d)\n", $$, $1, $3);
      }
    | concat
      { $$ = $1; }
    ;

/* Concaténation :
   - explicite via POINT
   - implicite (juxtaposition), même priorité que POINT
*/
concat:
      concat POINT repeat
      {
        $$ = state_count++;
        printf("a%d = concatenation(a%d, a%d)\n", $$, $1, $3);
      }
    | concat repeat  %prec POINT
      {
        $$ = state_count++;
        printf("a%d = concatenation(a%d, a%d)\n", $$, $1, $2);
      }
    | repeat
      { $$ = $1; }
    ;

/* Étoile de Kleene postfix, répétable (a**, etc.) */
repeat:
      repeat ETOILE
      {
        $$ = state_count++;
        printf("a%d = etoile(a%d)\n", $$, $1);
      }
    | atom
      { $$ = $1; }
    ;

/* Atomes : lettre, epsilon, parenthèses */
atom:
      LETTRE
      {
        $$ = state_count++;
        printf("a%d = automate(\"%c\")\n", $$, $1);
      }
    | EPS
      {
        $$ = state_count++;
        printf("a%d = automate(\"E\")\n", $$);
      }
    | PAR_G E PAR_D
      { $$ = $2; }
    | INCONNU
      {
        yyerror("Token inconnu dans l'expression");
        YYERROR;
      }
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Erreur syntaxique: %s\n", s);
}

int main(void) {
    return yyparse();
}
