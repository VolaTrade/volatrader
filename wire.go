//+build wireinject

package main

import (
	"context"

	"github.com/google/wire"
	"github.com/volatrade/volatrader/internal/config"
	"github.com/volatrade/volatrader/internal/handlers"

	logger "github.com/volatrade/currie-logs"
	stats "github.com/volatrade/k-stats"

	"github.com/volatrade/volatrader/internal/server"
	"github.com/volatrade/volatrader/internal/service"
)

var serviceModule = wire.NewSet(
	service.Module,
	wire.Bind(new(service.Service), new(*service.VolatraderService)),
)

func InitializeAndRun(ctx context.Context, cfg config.FilePath) (*server.Server, func(), error) {

	panic(
		wire.Build(
			config.NewConfig,
			config.NewServerConfig,
			config.NewStatsConfig,
			config.NewLoggerConfig,
			stats.New,
			logger.New,
			serviceModule,
			handlers.New,
			server.New,
		),
	)
}
