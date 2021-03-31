package config

import (
	"log"
	"strconv"

	"github.com/joho/godotenv"
	logger "github.com/volatrade/currie-logs"
	stats "github.com/volatrade/k-stats"

	"os"

	"github.com/volatrade/volatrader/internal/server"
	"github.com/volatrade/volatrader/internal/streamer"

	"github.com/volatrade/volatrader/internal/strategies"
)

//FilePath struct to be propogated through wire
type FilePath string

//Config ...
type Config struct {
	streamerConfig   streamer.Config
	serverConfig     server.Config
	statsConfig      stats.Config
	strategiesConfig strategies.Config
}

//NewConfig builds global config struct
func NewConfig(fileName FilePath) *Config {

	if err := godotenv.Load(string(fileName)); err != nil {
		log.Printf("Config file not found for file name: %s", fileName)
		panic(err)
	}

	env := os.Getenv("ENV")

	if env != "DEV" && env != "PRD" && env != "INTEG" {
		log.Println("ENV ==>", env)
		log.Fatal("ENV var in config.env isn't set properly")
	}

	return &Config{
		serverConfig: server.Config{
			Host:            os.Getenv("SERVER_HOST"),
			Port:            convertToInt(os.Getenv("SERVER_PORT")),
			ListenLimit:     convertToInt(os.Getenv("SERVER_LISTEN_LIMIT")),
			KeepAlive:       convertToInt(os.Getenv("SERVER_KEEP_ALIVE_TIME")),
			ReadTimeout:     convertToInt(os.Getenv("SERVER_READ_TIMEOUT")),
			WriteTimeout:    convertToInt(os.Getenv("SERVER_WRITE_TIMEOUT")),
			ShutdownTimeout: convertToInt(os.Getenv("SERVER_SHUTDOWN_TIME")),
		},
		strategiesConfig: strategies.Config{
			Host: os.Getenv("STRATEGIES_HOST"),
			Port: convertToInt(os.Getenv("STRATEGIES_PORT")),
		},
		streamerConfig: streamer.Config{
			CommunicatorCount: convertToInt(os.Getenv("COMMUNICATOR_COUNT")),
		},
	}
}

//NewServerConfig returns server config from global config
func NewServerConfig(cfg *Config) *server.Config {
	return &cfg.serverConfig
}

func NewLoggerConfig(cfg *Config) *logger.Config {
	return nil
}

func NewStatsConfig(cfg *Config) *stats.Config {
	log.Println("Stats config --->", cfg.statsConfig)
	return &cfg.statsConfig
}

func NewStrategiesConfig(cfg *Config) *strategies.Config {
	return &cfg.strategiesConfig
}

func NewStreamerConfig(cfg *Config) *streamer.Config {
	return &cfg.streamerConfig
}

func convertToInt(str string) int {
	intRep, err := strconv.Atoi(str)

	if err != nil {
		panic(err)
	}

	return intRep
}
