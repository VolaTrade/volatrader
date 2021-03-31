package service

import (
	"context"

	"github.com/volatrade/volatrader/internal/models"
	"github.com/volatrade/volatrader/internal/session"
	"github.com/volatrade/volatrader/internal/tsprocessor"
)

func (svc *VolatraderService) StartSessionRoutine(startRequest models.SessionStartRequest) (string, error) {

	ts := session.New(startRequest.StrategyID)

	//TODO validation
	var stopLoss, trailing bool
	var percent float64

	if startRequest.StopLoss != nil {
		stopLoss = true
		trailing = startRequest.StopLoss.Trailing
		percent = startRequest.StopLoss.Percent
	} else {
		stopLoss = false
		trailing = false
		percent = 0.0
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
		ts.Indicators[indicator] = nil
	}
	for _, indicator := range sellIndicators {
		ts.Indicators[indicator] = nil
	}
	stratClient, err := svc.strategies.Clone()

	if err != nil {
		return "", err
	}

	tsp := tsprocessor.New(svc.logger, stratClient, ts, buyIndicators, sellIndicators)
	svc.logger.Infow("Running session processor")

	svc.AddSession(buyIndicators, ts.SessionID.String(), tsp)
	svc.AddSession(sellIndicators, ts.SessionID.String(), tsp)

	for _, commStruct := range svc.commMap {

		commStruct.UpdateSessionMap(svc.indicatorSessions)
	}

	svc.sessionProcesses[ts.SessionID.String()] = tsp

	go tsp.Run(context.Background())

	return ts.SessionID.String(), nil
}

func (svc *VolatraderService) KillSessionRoutine(sessionID string) error {

	println("SessionID --> ", sessionID)
	svc.sessionProcesses[sessionID].Die <- true
	svc.DeleteTradeSession(sessionID)

	for _, commStruct := range svc.commMap {

		commStruct.UpdateSessionMap(svc.indicatorSessions)
	}

	return svc.strategies.DeleteStrategySession(sessionID)
}
