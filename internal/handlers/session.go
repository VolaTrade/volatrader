package handlers

import (
	"errors"
	"net/http"
	"time"

	"github.com/go-chi/render"
	"github.com/volatrade/go-errors/apierrors"
	"github.com/volatrade/volatrader/internal/models"
)

func (h *Handler) StartTradeSession(w http.ResponseWriter, r *http.Request) {

	sessionID, err := h.svc.StartSessionRoutine("ExampleStrategy")

	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		render.JSON(w, r, err.Error())
		return
	}
	w.WriteHeader(http.StatusOK)
	render.JSON(w, r, &models.SessionStartResponse{SessionID: sessionID, StartTime: time.Now()})
}

func (h *Handler) KillTradeSession(w http.ResponseWriter, r *http.Request) {

	sessionID, found := r.URL.Query()["session_id"]

	if !found {
		h.writeErrorResponse(w, r, apierrors.NewErrorResponse(errors.New("Param missing")))
	}

	if err := h.svc.KillSessionRoutine(sessionID[0]); err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		render.JSON(w, r, err.Error())
		return
	}
	w.WriteHeader(http.StatusOK)
}
