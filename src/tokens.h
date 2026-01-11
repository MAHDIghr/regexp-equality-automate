/* Ce fichier définit les tokens numériques utilisés UNIQUEMENT pour
 *  tester l'analyse lexicale (regexp.l) de manière indépendante. */

#ifndef TOKENS_H
#define TOKENS_H

/* Étape 1 : tokens numérotés */
#define LETTRE     101
#define EPS        102
#define PLUS       103
#define POINT      104
#define ETOILE     105
#define PAR_G      106
#define PAR_D     107
#define FIN_LIGNE  108
#define INCONNU   109

/* yylval minimal pour stocker une lettre */
typedef union {
    char c;
} YYSTYPE;

extern YYSTYPE yylval;

#endif
