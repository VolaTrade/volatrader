package strategies

import (
	"context"
	"log"

	"github.com/volatrade/protobufs/strategies/manager"
)

func (strat *StrategiesClient) RegisterStrategySession(sessionID string, strategyID string) ([]string, error) {

	resp, err := strat.managerClient.SpawnStrategy(
		context.Background(),
		&manager.SpawnRequest{
			SessionID:  sessionID,
			StrategyID: strategyID,
		},
	)
	if err != nil {
		return []string{}, err
	}

	log.Printf("%+v", resp)
	return resp.Indicators, nil
}
