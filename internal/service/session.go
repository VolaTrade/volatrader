package service

import (
	"context"

	"github.com/volatrade/volatrader/internal/models"
	"github.com/volatrade/volatrader/internal/session"
	"github.com/volatrade/volatrader/internal/tsprocessor"
)

func (svc *VolatraderService) StartSessionRoutine(startRequest models.SessionStartRequest) (string, error) {

	ts := session.New(startRequest.StrategyID)
	//register session with Strategy API
	stratIndicators, err := svc.strategies.
		RegisterStrategySession(
			ts.SessionID.String(),
			startRequest.StrategyID,
		)

	if err != nil {
		return "", err
	}

	for _, indicator := range stratIndicators {
		ts.Indicators[indicator] = nil
	}
	stratClient, err := svc.strategies.Clone()

	if err != nil {
		return "", err
	}

	tsp := tsprocessor.New(svc.logger, stratClient, ts)
	svc.logger.Infow("Running session processor")

	svc.AddSession(stratIndicators, ts.SessionID.String(), tsp)
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