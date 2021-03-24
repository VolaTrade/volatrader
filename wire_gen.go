// Code generated by Wire. DO NOT EDIT.

//go:generate wire
//+build !wireinject

package main

import (
	"context"
	"github.com/google/wire"
	"github.com/volatrade/currie-logs"
	"github.com/volatrade/k-stats"
	"github.com/volatrade/volatrader/internal/config"
	"github.com/volatrade/volatrader/internal/handlers"
	"github.com/volatrade/volatrader/internal/server"
	"github.com/volatrade/volatrader/internal/service"
	"github.com/volatrade/volatrader/internal/strategies"
)

// Injectors from wire.go:

func InitializeAndRun(ctx context.Context, cfg config.FilePath) (*server.Server, func(), error) {
	configConfig := config.NewConfig(cfg)
	serverConfig := config.NewServerConfig(configConfig)
	loggerConfig := config.NewLoggerConfig(configConfig)
	loggerLogger, cleanup, err := logger.New(loggerConfig)
	if err != nil {
		return nil, nil, err
	}
	statsConfig := config.NewStatsConfig(configConfig)
	statsStats, cleanup2, err := stats.New(statsConfig)
	if err != nil {
		cleanup()
		return nil, nil, err
	}
	strategiesConfig := config.NewStrategiesConfig(configConfig)
	strategiesClient, cleanup3, err := strategies.New(strategiesConfig, statsStats, loggerLogger)
	if err != nil {
		cleanup2()
		cleanup()
		return nil, nil, err
	}
	volatraderService := service.New(loggerLogger, statsStats, strategiesClient)
	handler, err := handlers.New(volatraderService, loggerLogger)
	if err != nil {
		cleanup3()
		cleanup2()
		cleanup()
		return nil, nil, err
	}
	serverServer, cleanup4, err := server.New(ctx, serverConfig, handler)
	if err != nil {
		cleanup3()
		cleanup2()
		cleanup()
		return nil, nil, err
	}
	return serverServer, func() {
		cleanup4()
		cleanup3()
		cleanup2()
		cleanup()
	}, nil
}

// wire.go:

var serviceModule = wire.NewSet(service.Module, wire.Bind(new(service.Service), new(*service.VolatraderService)))

var strategiesModule = wire.NewSet(strategies.Module, wire.Bind(new(strategies.Strategies), new(*strategies.StrategiesClient)))
