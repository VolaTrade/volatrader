package strategies

import (
	"context"

	"github.com/volatrade/go-errors/apierrors"
	"github.com/volatrade/protobufs/strategies/manager"
)

func (strat *StrategiesClient) DeleteStrategySession(sessionID string) error {

	resp, err := strat.managerClient.DeleteStrategy(
		context.Background(),
		&manager.DeletionRequest{
			SessionID: sessionID,
		},
	)

	if resp.Code == 5 {
		return apierrors.NewError(apierrors.NotFoundErrorType,
			"Session ID not found in Strategies API").
			WithExternalMessage("Session ID not found from Strategies API")
	}
	return err
}
