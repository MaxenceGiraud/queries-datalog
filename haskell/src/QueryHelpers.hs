module QueryHelpers where

import Query
import Syntax.QueryParser as P

programFromFile :: String -> IO (Either String Program)
programFromFile f =  P.parseProgram <$> readFile f

queryFromFile :: String -> IO (Either String Query)
queryFromFile f =  P.parseQuery <$> readFile f
