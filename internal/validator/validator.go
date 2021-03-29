package validator

type Validator interface {
	ValidateStrategyID(stratID string) error
}

type VTValidator struct {
}
