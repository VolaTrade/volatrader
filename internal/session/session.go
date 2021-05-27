package session

import (
	"errors"
	"fmt"
	"sync"

	"github.com/google/uuid"
)

type TradeSession struct {
	mux                *sync.RWMutex
	SessionID          uuid.UUID
	StrategyID         string
	BuyIndicators      map[string]interface{}
	BuyIndicatorCount  uint32
	SellIndicators     map[string]interface{}
	SellIndicatorCount uint32
	ValueMap           map[string]float64
	valueMapLength     uint32
}

func New(strategyID string) *TradeSession {
	return &TradeSession{
		mux:            &sync.RWMutex{},
		SessionID:      uuid.New(),
		StrategyID:     strategyID,
		ValueMap:       make(map[string]float64, 0),
		BuyIndicators:  make(map[string]interface{}, 0),
		SellIndicators: make(map[string]interface{}, 0),
	}
}

func (ts *TradeSession) ResetValueMap() {
	ts.mux.Lock()
	defer ts.mux.Unlock()
	ts.ValueMap = make(map[string]float64, 0)
	ts.valueMapLength = 0
}

//Checks to see if session is ready for an indicator update
func (ts *TradeSession) IndicatorsReadyForUpdate(posEntered bool) bool {
	ts.mux.RLock()
	defer ts.mux.RUnlock()

	if posEntered {
		return ts.valueMapLength == ts.SellIndicatorCount
	}
	return ts.valueMapLength == ts.BuyIndicatorCount
}

//InsertIndicatorValue inserts indicator value to trade sessions internal indicator value map
func (ts *TradeSession) InsertIndicator(indicator string, value float64, posEntered bool) error {
	ts.mux.RLock()
	var indicators map[string]interface{}
	if posEntered {
		indicators = ts.SellIndicators
	} else {
		indicators = ts.BuyIndicators
	}

	if _, exists := indicators[indicator]; !exists {
		ts.mux.RUnlock()
		return errors.New(fmt.Sprintf("Indicator not found for %s for session: %s", indicator, ts.SessionID))
	}

	ts.mux.RUnlock()
	ts.mux.Lock()
	ts.ValueMap[indicator] = value
	ts.mux.Unlock()
	return nil
}
