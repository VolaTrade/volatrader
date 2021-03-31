package service

import (
	"github.com/volatrade/volatrader/internal/models"
)

func (svc *VolatraderService) IndicatorUpdate(iu models.IndicatorUpdate) (*models.CommMessage, error) {

	message, err := svc.streamer.IndicatorUpdate(iu)

	if err != nil {
		return nil, err
	}

	return message, nil
}
