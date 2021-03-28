//go:generate mockgen -package=mocks -destination=../mocks/handlers.go github.com/Action-for-Racial-Justice/Cortex-backend/internal/handlers Handlers

package handlers

import (
	"fmt"
	"net/http"

	"github.com/go-chi/chi"
	"github.com/go-chi/chi/middleware"
	"github.com/go-chi/render"
	logger "github.com/volatrade/currie-logs"
	"github.com/volatrade/go-errors/apierrors"
	"github.com/volatrade/volatrader/internal/service"
)

//CortexHandler struct to hold relevant inner data members and hold functions for pure handler logic
type Handler struct {
	svc    service.Service
	logger *logger.Logger
	router *chi.Mux
}

//New ... constructor
func New(service service.Service, logger *logger.Logger) (*Handler, error) {
	handlers := &Handler{svc: service, logger: logger}
	router := chi.NewRouter()
	router.Use(middleware.Recoverer)
	router.Use(middleware.Logger)

	registerEndpoint("/health", router.Get, handlers.HealthCheck)
	registerEndpoint("/v1/session/start", router.Post, handlers.StartTradeSession)
	registerEndpoint("/v1/session/kill", router.Get, handlers.KillTradeSession)
	registerEndpoint("/v1/indicators/update", router.Post, handlers.IndicatorUpdate)
	handlers.router = router

	return handlers, nil
}

// ServeHTTP serves a http request given a response builder and request
func (h *Handler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	h.router.ServeHTTP(w, r)
}

//registerEndpoint registers an endpoint to the router for a specified method type and handlerFunction
func registerEndpoint(endpoint string, routeMethod func(pattern string, handlerFn http.HandlerFunc), handlerFunc func(w http.ResponseWriter, r *http.Request)) {
	routeMethod(endpoint, http.HandlerFunc(handlerFunc).ServeHTTP)
}

func (h *Handler) writeErrorResponse(w http.ResponseWriter, r *http.Request, errResp *apierrors.ErrorResponse) {
	for _, err := range errResp.Errors {
		h.logger.Errorw(fmt.Sprintf("request failed %v", err.RootCauseError),
			"error id", err.ID,
			"error type", err.Type,
			"message", err.InternalMessage)
	}

	render.Status(r, errResp.StatusCode)
	render.JSON(w, r, errResp)
}
