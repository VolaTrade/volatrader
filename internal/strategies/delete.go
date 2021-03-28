package strategies

import (
	"context"
	"log"

	"github.com/volatrade/protobufs/strategies/manager"
)

func (strat *StrategiesClient) DeleteStrategySession(sessionID string) error {

	resp, err := strat.managerClient.DeleteStrategy(
		context.Background(),
		&manager.DeletionRequest{
			SessionID: sessionID,
		},
	)

	log.Printf("%+v", resp)
	return err
}
