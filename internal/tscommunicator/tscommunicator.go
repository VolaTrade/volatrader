//tsprocessor --> Trade Session Communication package
package tscommunicator

import (
	"errors"
	"fmt"
	"sync"

	"context"

	"github.com/google/uuid"
	logger "github.com/volatrade/currie-logs"
	"github.com/volatrade/volatrader/internal/models"
	"github.com/volatrade/volatrader/internal/tsprocessor"
)

type TSCommunicator interface {
}

type VTTSCommunicator struct {
	id                  uuid.UUID
	logger              *logger.Logger
	mux                 *sync.RWMutex
	indicatorSessionMap map[string]map[string]*tsprocessor.TSProcessor
	serviceChan         chan models.IndicatorUpdate
	relayChannel        chan models.CommMessage
}

func New(id uuid.UUID, logger *logger.Logger,
	svcChan chan models.IndicatorUpdate, relayChannel chan models.CommMessage) *VTTSCommunicator {
	return &VTTSCommunicator{
		id:                  id,
		logger:              logger,
		mux:                 &sync.RWMutex{},
		relayChannel:        relayChannel,
		serviceChan:         svcChan,
		indicatorSessionMap: make(map[string]map[string]*tsprocessor.TSProcessor, 0),
	}

}

func (com *VTTSCommunicator) UpdateSessionMap(newMap map[string]map[string]*tsprocessor.TSProcessor) {
	com.mux.Lock()
	com.indicatorSessionMap = newMap
	com.mux.Unlock()
}

func (com *VTTSCommunicator) WaitAndSlave(ctx context.Context) {
	com.logger.Infow("Starting communicator slave process", "ID", com.id.String())
	for {
		select {

		case <-ctx.Done():
			return

		case update := <-com.serviceChan:
			relayMessage := models.CommMessage{ID: com.id.String()}
			com.mux.RLock()
			if sessionProcMap, ok := com.indicatorSessionMap[update.Indicator]; ok {
				for _, tradeProcess := range sessionProcMap {
					tradeProcess.UpdateChan <- update
				}
			} else {
				relayMessage.Error = errors.New(fmt.Sprintf("Could not find indicator %s", update.Indicator))
			}
			com.mux.RUnlock()
			com.relayChannel <- relayMessage

		}
	}
}
