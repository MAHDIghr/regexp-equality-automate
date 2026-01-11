#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#include "../src/tokens.h"

extern int yylex(void);
extern FILE* yyin;
extern char* yytext;

YYSTYPE yylval;

int main(void)
{
    yyin = fopen("test_lexer.txt", "r");
    assert(yyin && "Impossible d'ouvrir test_lexer.txt");

    int token;
    while ((token = yylex()) != 0)
    {
        if (token == INCONNU) {
            printf("❌ le token '%s' n'est pas reconnu\n", yytext);
        } else if (token == FIN_LIGNE) {
            //afficher les fins de lignes
            printf("— fin de ligne —\n");
        } else {
            printf("✅ le token '%s' est reconnu\n", yytext);
        }
    }

    fclose(yyin);

    return 0;
}
