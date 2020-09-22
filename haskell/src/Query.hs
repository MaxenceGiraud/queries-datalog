module Query where

import Data.List

data Term
  = Var String
  | Any
  | Const String

concatWith :: (Show a) => String -> [a] -> String
concatWith sep l = concat $ intersperse sep $ show <$> l

concatComma :: (Show a) => [a] -> String
concatComma = concatWith ","

concatLine :: (Show a) => [a] -> String
concatLine = concatWith "\n"


instance Show(Term) where
  show (Var s) = s
  show (Const s) = s
  show Any = "_"

data Predicate
  = Predicate String [Term]
  | NegPredicate String [Term]
  | Equal Term Term
  | NEqual Term Term

instance Show(Predicate) where
  show (Predicate n t) = n ++ "(" ++ concatComma t ++ ")"

  show (NegPredicate n t) ="¬" ++ n ++ "(" ++ concatComma t ++ ")"

  show (Equal t1 t2) = show t1 ++ " = " ++ show t2

  show (NEqual t1 t2) = show t1 ++ " ≠ " ++ show t2


data SPredicate
  = SPredicate String [Term]

instance Show(SPredicate) where
  show (SPredicate n t) = n ++ "(" ++ concatComma t ++ ")"

data Fact
  = Fact String [String]

instance Show(Fact) where
  show (Fact n t) = n ++ "(" ++ concatComma t ++ ")"

data Rule = Rule
  { head :: SPredicate,
    body :: [Predicate]
  }

instance Show(Rule) where
  show r = case body r of
             [] -> show (Query.head r) ++ "."
             _  -> show (Query.head r) ++ " ← " ++ concatWith " " (body r) ++ "."

newtype Program = Program [Rule]

instance Show(Program) where
  show (Program rules)= concatLine rules



data Query = Query
  { query :: SPredicate,
    program :: Program,
    database :: [Fact]
  }

instance Show(Query) where
  show q = show (program q) ++ "\n\n" ++ concatLine (database q) ++ "\n\n" ++ "? " ++ show(query q)
