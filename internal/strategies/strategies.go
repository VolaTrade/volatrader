package strategies

import (
	"context"
	"fmt"
	"log"

	"github.com/google/wire"
	logger "github.com/volatrade/currie-logs"
	stats "github.com/volatrade/k-stats"
	exec "github.com/volatrade/protobufs/strategies/executor"
	manager "github.com/volatrade/protobufs/strategies/manager"
	"google.golang.org/grpc"
)

var Module = wire.NewSet(
	New,
)

type (
	Strategies interface {
	}
	Config struct {
		Port int
		Host string
	}
	StrategiesClient struct {
		conn           *grpc.ClientConn
		config         *Config
		kstats         stats.Stats
		logger         *logger.Logger
		managerClient  manager.ManagerClient
		executorClient exec.ExecutorClient
	}
)

func New(cfg *Config, kstats stats.Stats, logger *logger.Logger) (*StrategiesClient, func(), error) {

	log.Println("creating client connection to strategies -> port:", cfg.Port)
	conn, err := grpc.Dial(fmt.Sprintf(":%d", cfg.Port), grpc.WithInsecure())
	if err != nil {
		log.Printf("did not connect: %s", err)
		return nil, nil, err
	}
	managerClient := manager.NewManagerClient(conn)
	executorClient := exec.NewExecutorClient(conn)
	end := func() {
		if conn != nil {
			if err := conn.Close(); err != nil {
				log.Printf("Error closing client connection to strategies: %v", err)
			}
			log.Println("Successful Shutdown of client connection to strategies")
		}
	}

	return &StrategiesClient{
		managerClient:  managerClient,
		executorClient: executorClient,
		conn:           conn,
		config:         cfg,
		kstats:         kstats,
		logger:         logger,
	}, end, nil
}
