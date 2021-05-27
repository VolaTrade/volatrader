package validator

import (
	"strings"

	"github.com/volatrade/go-errors/apierrors"
)

func (v *VTValidator) ValidateStrategyID(stratID string) error {

	if stratID == "" || !strings.Contains(stratID, "strategy") {
		return apierrors.NewError(
			apierrors.ValidationErrorType,
			"provided strategy ID is invalid").
			WithExternalMessage("strategy ID must not be blank and contain substring strategy")
	}
	return nil
}
