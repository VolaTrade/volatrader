package handlers

import (
	"encoding/json"
	"net/http"

	"github.com/go-chi/render"
	"github.com/volatrade/go-errors/apierrors"
	"github.com/volatrade/volatrader/internal/models"
)

func (h *Handler) IndicatorUpdate(w http.ResponseWriter, r *http.Request) {
	var update models.IndicatorUpdate
	if err := json.NewDecoder(r.Body).Decode(&update); err != nil {
		h.writeErrorResponse(w, r, apierrors.CreateJSONDecodeErrorResponse(err))
		return
	}

	commResponse, err := h.svc.IndicatorUpdate(update)

	if err != nil {
		h.writeErrorResponse(w, r, apierrors.NewErrorResponse(err))
		return
	}

	render.JSON(w, r, commResponse)
}
