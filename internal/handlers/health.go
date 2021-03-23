package handlers

import (
	"net/http"

	"github.com/go-chi/render"
)

func (h *Handler) HealthCheck(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	render.JSON(w, r, nil)
}
