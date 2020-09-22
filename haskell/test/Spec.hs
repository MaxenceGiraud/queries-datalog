module Spec where

import QueryHelpers

main :: IO ()
main = do
  r <- queryFromFile "./test/test.datalog"
  case r of
    Left s -> putStrLn s
    Right p -> putStrLn $ show p
