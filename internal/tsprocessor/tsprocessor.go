// tsprocessor --> Trade Session Processor
package tsprocessor

import (
	"context"

	logger "github.com/volatrade/currie-logs"
	"github.com/volatrade/volatrader/internal/models"
	"github.com/volatrade/volatrader/internal/session"
	"github.com/volatrade/volatrader/internal/strategies"
)

type TSProcessor struct {
	tradingPair     string
	die             chan bool
	positionEntered bool
	logger          *logger.Logger
	session         *session.TradeSession
	updateChan      chan models.IndicatorUpdate
	stratClient     strategies.Strategies
	buyIndicators   []string
	sellIndicators  []string
}

func New(logger *logger.Logger, stratClient strategies.Strategies, die chan bool,
	updateChan chan models.IndicatorUpdate, session *session.TradeSession,
	buyIndicators []string, sellIndicators []string, pair string) *TSProcessor {

	return &TSProcessor{
		tradingPair:     pair,
		buyIndicators:   buyIndicators,
		sellIndicators:  sellIndicators,
		die:             die,
		positionEntered: false,
		logger:          logger,
		session:         session,
		updateChan:      updateChan,
		stratClient:     stratClient,
	}
}

func (tsp *TSProcessor) handleIndicatorUpdate(update models.IndicatorUpdate) error {

	if err := tsp.session.InsertIndicator(update.Indicator, update.Value, tsp.positionEntered); err != nil {
		tsp.logger.Errorw(err.Error())
		return err
	}
	return nil
}

func (tsp *TSProcessor) handleSessionUpdate() error {

	conditionsMet, err := tsp.stratClient.
		ExecuteStrategyUpdate(tsp.session.SessionID.String(),
			tsp.session.ValueMap,
			!tsp.positionEntered,
		)
	tsp.session.ResetValueMap()

	if err != nil {
		return err
	}

	if conditionsMet {

		tsp.positionEntered = !tsp.positionEntered
		//SEND UPDATE REQUEST TO EXTERNAL API
		tsp.logger.Infow("Stratey logic returned true",
			"Trade session", tsp.session.SessionID,
			"Strategy", tsp.session.StrategyID,
			"Position entered", tsp.positionEntered,
		)
	}

	return nil

}

func (tsp *TSProcessor) Run(ctx context.Context) {

	for {
		select {

		case update := <-tsp.updateChan:

			if err := tsp.handleIndicatorUpdate(update); err != nil {
				continue
			}
			if tsp.session.IndicatorsReadyForUpdate(tsp.positionEntered) {
				if err := tsp.handleSessionUpdate(); err != nil {
					tsp.logger.Errorw(err.Error())
				}
			}

		case <-tsp.die:
			tsp.logger.Infow("Received death request", "Trade session", tsp.session.SessionID)
			return

		case <-ctx.Done():
			return

		}
	}
}
