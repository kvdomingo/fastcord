package models

type CreateGuildInput struct {
	Name   string  `json:"name" validate:"required"`
	Avatar *string `json:"avatar" validate:"omitempty,url"`
	Banner *string `json:"banner" validate:"omitempty,url"`
}
