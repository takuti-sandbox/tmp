package main

import (
  "log"
)

func main() {
  log.Print("start")

  for i:=0; i<10; i++ {
      go func(i int) {
          log.Print(i)
      }(i)
  }

  log.Print("end")
}
