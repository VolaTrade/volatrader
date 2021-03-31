package strategies

import (
	"context"
	"log"

	"github.com/volatrade/protobufs/strategies/manager"
)

func (strat *StrategiesClient) RegisterStrategySession(sessionID string, strategyID string,
	stopLoss bool, trailing bool, percent float64) ([]string, []string, error) {

	resp, err := strat.managerClient.SpawnStrategy(
		context.Background(),
		&manager.SpawnRequest{
			SessionID:  sessionID,
			StrategyID: strategyID,
			StopLoss:   stopLoss,
			Trailing:   trailing,
			Percent:    percent,
		},
	)
	if err != nil {
		return []string{}, []string{}, err
	}

	log.Printf("%+v", resp)
	return resp.BuyIndicators, resp.SellIndicators, nil
}
