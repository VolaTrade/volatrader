package service

import (
	"fmt"
	"time"

	"github.com/volatrade/go-errors/apierrors"
	"github.com/volatrade/volatrader/internal/models"
	"github.com/volatrade/volatrader/internal/tsprocessor"
)

func (svc *VolatraderService) IndicatorUpdate(iu models.IndicatorUpdate) (*models.CommMessage, error) {

	svc.commChannel <- iu
	timer := time.NewTimer(1 * time.Second)
	defer timer.Stop()
	select {

	case commMessage := <-svc.relayChannel:
		return &commMessage, nil

	case <-timer.C:
		return nil, apierrors.NewError(
			apierrors.InternalErrorType,
			"Timeout trying to wait for verification").
			WithExternalMessage(fmt.Sprintf("Indicator update failed: %+v", iu))
	}

}

func (svc *VolatraderService) AddSession(indicators []string, sessionID string,
	sessionProcessor *tsprocessor.TSProcessor,
) {
	for _, indicator := range indicators {

		if _, ok := svc.indicatorSessions[indicator]; !ok {
			svc.indicatorSessions[indicator] = make(map[string]*tsprocessor.TSProcessor, 0)
		}
		svc.indicatorSessions[indicator][sessionID] = sessionProcessor
	}
}

func (svc *VolatraderService) DeleteTradeSession(sessionID string) {

	for _, sessionProcMap := range svc.indicatorSessions {

		if _, ok := sessionProcMap[sessionID]; ok {
			delete(sessionProcMap, sessionID)
		}
	}
}
