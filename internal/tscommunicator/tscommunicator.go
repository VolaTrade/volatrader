//tsprocessor --> Trade Session Communication package
package tscommunicator

import (
	"sync"

	"github.com/google/uuid"
	"github.com/volatrade/volatrader/internal/models"
	"github.com/volatrade/volatrader/internal/tsprocessor"

	logger "github.com/volatrade/currie-logs"
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

func (com *VTTSCommunicator) WaitAndSlave() {
	com.logger.Infow("Starting communicator slave process", "ID", com.id.String())
	for {
		select {
		case update := <-com.serviceChan:

			com.mux.RLock()
			if sessionProcMap, ok := com.indicatorSessionMap[update.Indicator]; ok {

				for _, tradeProcess := range sessionProcMap {
					tradeProcess.UpdateChan <- update
				}
			}
			com.mux.RUnlock()
			com.relayChannel <- models.CommMessage{ID: com.id.String(), Error: nil}

		}
	}
}
