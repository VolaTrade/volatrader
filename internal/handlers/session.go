package handlers

import (
	"encoding/json"
	"errors"
	"net/http"
	"time"

	"github.com/go-chi/render"
	"github.com/volatrade/go-errors/apierrors"
	"github.com/volatrade/volatrader/internal/models"
)

func (h *Handler) StartTradeSession(w http.ResponseWriter, r *http.Request) {

	var startRequest models.SessionStartRequest

	if err := json.NewDecoder(r.Body).Decode(&startRequest); err != nil {
		w.WriteHeader(http.StatusBadRequest)
		render.JSON(w, r, apierrors.CreateJSONDecodeErrorResponse(err))
		return
	}

	sessionID, err := h.svc.StartSessionRoutine(startRequest)

	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		render.JSON(w, r, err.Error())
		return
	}
	w.WriteHeader(http.StatusOK)
	render.JSON(w, r, &models.SessionStartResponse{SessionID: sessionID, StartTime: time.Now()})
}

func (h *Handler) KillTradeSession(w http.ResponseWriter, r *http.Request) {

	sessionIDs, found := r.URL.Query()["session_id"]

	if !found {
		h.writeErrorResponse(w, r, apierrors.NewErrorResponse(errors.New("Param missing")))
	}

	if err := h.svc.KillSessionRoutine(sessionIDs[0]); err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		render.JSON(w, r, err.Error())
		return
	}
	w.WriteHeader(http.StatusOK)
}
