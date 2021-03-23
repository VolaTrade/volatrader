package main

import (
	"context"
	"log"
)

func main() {
	server, stop, err := InitializeAndRun(context.Background(), "config.env")

	if err != nil {
		log.Println("Error obtained trying to start server ", err)
		panic(err)
	}
	server.Stop(stop)
}