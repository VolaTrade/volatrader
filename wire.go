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
	"github.com/volatrade/volatrader/internal/strategies"
)

var serviceModule = wire.NewSet(
	service.Module,
	wire.Bind(new(service.Service), new(*service.VolatraderService)),
)

var strategiesModule = wire.NewSet(
	strategies.Module,
	wire.Bind(new(strategies.Strategies), new(*strategies.StrategiesClient)),
)

func InitializeAndRun(ctx context.Context, cfg config.FilePath) (*server.Server, func(), error) {

	panic(
		wire.Build(
			config.NewConfig,
			config.NewServerConfig,
			config.NewStatsConfig,
			config.NewLoggerConfig,
			config.NewStrategiesConfig,
			config.NewServiceConfig,
			stats.New,
			logger.New,
			serviceModule,
			strategiesModule,
			handlers.New,
			server.New,
		),
	)
}
