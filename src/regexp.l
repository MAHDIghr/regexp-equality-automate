%{
#include <stdio.h>
#include <stdlib.h>
#include "regexp.tab.h"
%}

%%
[abc]           { yylval.c = yytext[0]; return LETTRE; }

"E"             { return EPS; }          /* epsilon */

"+"             { return PLUS; }
"."             { return POINT; }        /* concat explicite (facultatif au niveau grammaire) */
"*"             { return ETOILE; }

"("             { return PAR_G; }
")"             { return PAR_D; }

\r?\n         { return FIN_LIGNE; }    /* gère \n et \r\n */

[ \t]+          ;                        /* ignore espaces / tabs */

.               { return INCONNU; }
%%

int yywrap(void) { return 1; }
