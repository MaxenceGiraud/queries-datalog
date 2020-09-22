{
module Syntax.QueryParser where
import Syntax.QueryLexer
import Query as Q
}

%name pQuery Query
%name pProgram Program
%tokentype { Token }
%lexer  {lexWrap} {Eof}
%monad {Alex}
%error {parseError}

%token
',' {Conj _ _}
'¬'  {Neg _ _}
'←' {Impl _ _}
var {Variable _ _}
'_' {Anything _ _}
name {Name _ _}
'(' {Lpar _ _}
')' {Rpar _ _}
'.' {Dot _ _}
'=' {EQUAL _ _}
'?' {Ask _ _}
'≠' {NOTEQUAL _ _}

%%
Query: Program TheQuery {Q.Query $2 (Q.Program $1) []}

Program: Rule Program {$1:$2}
| Rule {[$1]}

Rule: Head '←' Body '.' {Q.Rule $1 $3}
| Head '.' {Q.Rule $1 []}

Head: Pred '(' Args ')' {Q.SPredicate $1 $3}

Pred: var {writting $1}
| name    {writting $1}

Args:  {[]}
| NArgs {$1}

NArgs: Term {[$1]}
| Term ',' NArgs {$1 : $3}
| Term NArgs {$1 : $2}

Body: {[]}
| Clause ',' Body {$1:$3}
| Clause Body {$1:$2}

Term:  var {Q.Var $ writting $1}
| name {Q.Const $ writting $1}
| '_' {Q.Any}

TTerm:  var {Q.Var $ writting $1}
| name {Q.Const $ writting $1}

Clause: TTerm '=' TTerm {Q.Equal $1 $3}
  | '¬' TTerm '=' TTerm {Q.NEqual $2 $4}
  | TTerm '≠' TTerm {Q.NEqual $1 $3}
  | '¬' Pred '(' Args ')' {Q.NegPredicate $2 $4}
  | Pred '(' Args ')' {Q.Predicate $1 $3}

TheQuery: '?' Head '.' {$2}
| '?' Head {$2}


{
parseError ::Token -> Alex a
parseError Eof = alexError $ "Unexpected End of File"
parseError t = alexError $ "Parse error.  Line: " ++ show l++ ", Col: " ++ show c
  where AlexPn _ l c = pos t

parseProgram :: String -> Either String Program
parseProgram s =  case runAlex s pProgram of
                   Left s -> Left s
                   Right p -> Right $ Q.Program p


parseQuery :: String -> Either String Query
parseQuery s =  runAlex s pQuery
}

