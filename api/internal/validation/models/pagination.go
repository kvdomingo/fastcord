package models

type PaginationParams struct {
	Page     int `json:"page" validate:"gte=1"`
	PageSize int `json:"page_size" validate:"gte=1,lte=50"`
}
