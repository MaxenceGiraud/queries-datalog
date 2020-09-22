{
module Syntax.QueryLexer where
}

%wrapper "monad"

@conj = ","
@neg = "~" | \! | ¬
@impl = "<=" | "<-" | ← | ":-"
@ask = "?" | "?-"
@neq = "<>" | "~=" | "!=" | "≠"
$upper = [A-Z]
$lower = [a-z]
$letters = [a-zA-Z0-9]
$symbols = [$letters\-_]
@var = $upper $symbols*
@name = $lower $symbols* | "'" ([^\'] | \\\')+ "'" | \" ([^\"] | \\\")+ \"



tokens :-
$white+ ;
@conj {mkT Conj}
@neg  {mkT Neg}
@impl {mkT Impl}
@var  {mkT Variable}
"_"   {mkT Anything}
@name {mkT Name}
"."   {mkT Dot}
"("   {mkT Lpar}
")"   {mkT Rpar}
"="   {mkT EQUAL}
@ask  {mkT Ask}
@neq  {mkT NOTEQUAL}

{

mkT :: (String -> AlexPosn -> Token) -> AlexInput -> Int -> Alex Token
mkT cst (p, _, _, str) len = return $ cst t p
    where t = take len str

alexEOF :: Alex Token
alexEOF = return Eof

data Token = Conj {writting :: String, pos :: AlexPosn}
     | Neg {writting :: String, pos :: AlexPosn}
     | Impl {writting :: String, pos :: AlexPosn}
     | Variable  {writting :: String, pos :: AlexPosn}
     | Anything {writting :: String, pos :: AlexPosn}
     | Name {writting :: String, pos :: AlexPosn}
     | Lpar {writting :: String, pos :: AlexPosn}
     | Rpar {writting :: String, pos :: AlexPosn}
     | Dot {writting :: String, pos :: AlexPosn}
     | EQUAL {writting :: String, pos :: AlexPosn}
     | NOTEQUAL {writting :: String, pos :: AlexPosn}
     | Ask {writting :: String, pos :: AlexPosn}
     | Eof

lexWrap :: (Token -> Alex a) -> Alex a
lexWrap = (alexMonadScan >>=)
}
