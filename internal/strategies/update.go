package strategies

import (
	"context"

	"github.com/volatrade/protobufs/strategies/executor"
)

func (strat *StrategiesClient) ExecuteStrategyUpdate(sessionID string, stratParams map[string]float64, buyUpdate bool) (bool, error) {
	resp, err := strat.executorClient.
		ExecuteStrategyUpdate(
			context.Background(),
			&executor.ExecuteRequest{
				SessionID:   sessionID,
				StratParams: stratParams,
				BuyUpdate:   buyUpdate,
			},
		)

	if err != nil {
		return false, err
	}

	return resp.Value, nil
}
