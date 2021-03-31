package session

import (
	"errors"
	"fmt"
	"sync"

	"github.com/google/uuid"
)

type TradeSession struct {
	mux            *sync.RWMutex
	SessionID      uuid.UUID
	StrategyID     string
	BuyIndicators  map[string]interface{}
	SellIndicators map[string]interface{}
	indicatorCount uint32
	ValueMap       map[string]float64
	valueMapLength uint32
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

func (ts *TradeSession) LengthsEqual() bool {
	return ts.valueMapLength == ts.indicatorCount
}

func (ts *TradeSession) InsertValue(indicator string, value float64, posEntered bool) error {
	ts.mux.RLock()
	indicators := ts.BuyIndicators
	if posEntered {
		indicators = ts.SellIndicators
	}
	
	if _, exists := indicators[indicator]; !exists {
		ts.mux.RUnlock()
		return errors.New(fmt.Sprintf("Indicator not found for %s for session: %s", indicator, ts.SessionID))
	}

	ts.mux.RUnlock()
	ts.mux.Lock()
	defer ts.mux.Unlock()
	ts.ValueMap[indicator] = value
	return nil
}

// func (ts *TradeSession) IndicatorsAreReady() bool {
// 	ts.mux.RLock()
// 	defer ts.mux.RUnlock()
// 	//map to map comparison for O(N) best case look up
// 	for key, _ := range ts.Indicators {
// 		if _, exists := ts.valueMap[key]; !exists {
// 			return false
// 		}
// 	}
// 	return true
// }
