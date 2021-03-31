package tscommunicator

import (
	"context"
	"testing"
	"time"

	"github.com/google/uuid"
	"github.com/stretchr/testify/assert"
	logger "github.com/volatrade/currie-logs"
	"github.com/volatrade/volatrader/internal/models"
)

type testSuite struct {
	updateChan   chan models.IndicatorUpdate
	relayChan    chan models.CommMessage
	communicator *VTTSCommunicator
	commID       uuid.UUID
}

func createTestSuite() *testSuite {
	logger := logger.NewNoop()
	id := uuid.New()
	updateChan := make(chan models.IndicatorUpdate)
	relayChan := make(chan models.CommMessage)
	comm := New(id, logger, updateChan, relayChan)

	return &testSuite{updateChan: updateChan, relayChan: relayChan, communicator: comm, commID: id}
}

func TestWaitAndSlaveRelay(t *testing.T) {
	ts := createTestSuite()
	ctx, cancel := context.WithCancel(context.Background())
	timer := time.NewTicker(time.Second * 1)

	go ts.communicator.WaitAndSlave(ctx)
	ts.updateChan <- models.IndicatorUpdate{}

	defer timer.Stop()
	defer cancel()
	select {

	case <-timer.C:
		assert.Fail(t, "timeout")
		break
	case relayMessage := <-ts.relayChan:
		assert.Equal(t, relayMessage.ID, ts.commID.String())
		break
	}
}

func TestWaitAndSlaveRelayIndicatorDNE(t *testing.T) {
	ts := createTestSuite()
	ctx, cancel := context.WithCancel(context.Background())
	timer := time.NewTicker(time.Second * 1)

	go ts.communicator.WaitAndSlave(ctx)
	ts.updateChan <- models.IndicatorUpdate{Indicator: "EMA"}

	defer timer.Stop()
	defer cancel()
	select {

	case <-timer.C:
		assert.Fail(t, "timeout")
		break
	case relayMessage := <-ts.relayChan:
		assert.Equal(t, relayMessage.ID, ts.commID.String())
		assert.Error(t, relayMessage.Error)
		break
	}

}
