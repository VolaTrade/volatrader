package service

import (
	"context"

	"github.com/volatrade/go-errors/apierrors"
	"github.com/volatrade/volatrader/internal/models"
	"github.com/volatrade/volatrader/internal/session"
	"github.com/volatrade/volatrader/internal/tsprocessor"
)

func (svc *VolatraderService) StartSessionRoutine(startRequest models.SessionStartRequest) (string, error) {

	ts := session.New(startRequest.StrategyID)

	//TODO validation
	var stopLoss, trailing bool = false, false
	var percent float64 = 0.0

	if startRequest.StopLoss != nil {
		stopLoss = true
		trailing = startRequest.StopLoss.Trailing
		percent = startRequest.StopLoss.Percent
	}
	//register session with Strategy API
	buyIndicators, sellIndicators, err := svc.strategies.
		RegisterStrategySession(
			ts.SessionID.String(),
			startRequest.StrategyID,
			stopLoss,
			trailing,
			percent,
		)

	if err != nil {
		return "", err
	}

	for _, indicator := range buyIndicators {
		ts.BuyIndicators[indicator] = nil
	}
	for _, indicator := range sellIndicators {
		ts.SellIndicators[indicator] = nil
	}
	stratClient, err := svc.strategies.Clone()

	if err != nil {
		return "", err
	}

	updateChan := make(chan models.IndicatorUpdate)
	deathChan := make(chan bool)
	tsp := tsprocessor.New(svc.logger, stratClient, deathChan,
		updateChan, ts, buyIndicators, sellIndicators, startRequest.Pair,
	)
	svc.logger.Infow("Running session processor")

	indicators := append(buyIndicators, sellIndicators...)

	svc.streamer.AddSession(indicators, ts.SessionID.String(),
		updateChan, deathChan, startRequest.Pair)
	go tsp.Run(context.Background())

	return ts.SessionID.String(), nil
}

func (svc *VolatraderService) KillSessionRoutine(sessionID string) error {

	if err := svc.strategies.DeleteStrategySession(sessionID); err != nil {
		return apierrors.NewError(
			apierrors.InternalErrorType,
			"Error deleting stratgy from strategies API").
			WithExternalMessage("Could not delete strategy from Strategies API").
			WithRootCauseError(err)
	}
	svc.streamer.DeleteTradeSession(sessionID)
	return nil
}
