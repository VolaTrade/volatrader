package server

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/volatrade/volatrader/internal/handlers"
)

type (
	// Config ...
	Config struct {
		Host            string
		Port            int
		ListenLimit     int
		KeepAlive       int
		ReadTimeout     int
		WriteTimeout    int
		ShutdownTimeout int
	}

	//Server struct to hold http server
	Server struct {
		Cfg        *Config
		serverHTTP *http.Server
	}
)

//New ... server constructor
func New(ctx context.Context, cfg *Config, apiHandlers *handlers.Handler) (*Server, func(), error) {

	restServer := initializeServer(cfg, apiHandlers)
	go spawnServer(restServer)

	stop := func() {
		log.Println("starting to shutdown REST API HTTP server")

		ctx, cancel := context.WithTimeout(context.Background(), time.Duration(cfg.ShutdownTimeout)*time.Second)
		if err := restServer.serverHTTP.Shutdown(ctx); err != nil {
			log.Println("failed to shutdown REST API HTTP server")
			panic(err)
		}

		defer cancel()
	}

	return restServer, stop, nil
}

func spawnServer(server *Server) {
	log.Printf("starting REST API HTTP server @ %s:%d", server.Cfg.Host, server.Cfg.Port)

	if err := server.serverHTTP.ListenAndServe(); err != http.ErrServerClosed {

		log.Printf("failed to run REST API HTTP server at address %s", server.serverHTTP.Addr)
		panic(err)
	}
}

func initializeServer(config *Config, handler http.Handler) *Server {

	return &Server{
		Cfg: config,
		serverHTTP: &http.Server{
			Addr:         fmt.Sprintf("%s:%d", config.Host, config.Port),
			Handler:      handler,
			ReadTimeout:  time.Duration(10) * time.Second,
			WriteTimeout: time.Duration(10) * time.Second,
		},
	}
}

// returns a channel to handle shutdown
func (sv *Server) done() <-chan os.Signal {
	sigs := make(chan os.Signal, 1)
	signal.Notify(sigs, syscall.SIGINT, syscall.SIGTERM)
	return sigs
}

//Stop waits for shutdown signal from shutdown cahnnel
func (sv *Server) Stop(stop func()) {
	done := <-sv.done()
	log.Printf("Received shutdown OS signal : --%s--", done.String())
	stop()
	os.Exit(0)
}
