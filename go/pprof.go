package main

import (
    "fmt"
    "net"
    "net/http"
    _ "net/http/pprof"
)

func fib(n int) int {
    if n < 2 {
        return n
    }
    return fib(n-1) + fib(n-2)
}

func main() {
    l, err := net.Listen("tcp", ":0")
    if err != nil {
        panic(err)
    }
    fmt.Printf("Listening on %s\n", l.Addr())
    go http.Serve(l, nil)

    for {
        fib(27)
        fib(28)
        fib(29)
        fib(30)
    }
}
