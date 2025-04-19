package controllers

import (
	"context"
	"fastcord/database"
	"fastcord/internal/sql"
	"fastcord/internal/validation"
	"fastcord/internal/validation/models"
	"fmt"
	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/log"
	"github.com/jackc/pgx/v5/pgtype"
	"strconv"
)

// RetrieveGuilds godoc
// @Summary List all guilds
// @Tags guild
// @Accept json
// @Produce json
// @Param page query int false "Page number"
// @Param page_size query int false "Page size"
// @Success 200
// @Failure 400 {object} validation.ErrorResponse
// @Router /guilds [get]
func RetrieveGuilds(ctx *fiber.Ctx) error {
	var err error
	var errResp []validation.ErrorResponse

	var queryParams models.PaginationParams
	err = ctx.QueryParser(&queryParams)
	if err != nil {
		return fmt.Errorf("error parsing query params: %v", err)
	}

	page, err := strconv.ParseInt(ctx.Query("page", "1"), 10, 32)
	if err != nil {
		return fmt.Errorf("error parsing `page`: %v", err)
	}

	pageSize, err := strconv.ParseInt(ctx.Query("page_size", "10"), 10, 32)
	if err != nil {
		return fmt.Errorf("error parsing `page_size`: %v", err)
	}

	queries := models.PaginationParams{
		Page:     int(page),
		PageSize: int(pageSize),
	}
	err = ctx.QueryParser(&queries)
	if err != nil {
		return fmt.Errorf("error parsing query params: %v", err)
	}

	validator := validation.GetValidatorInstance()
	errResp = validator.Validate(queries)
	if len(errResp) > 0 {
		return ctx.Status(fiber.StatusBadRequest).JSON(errResp)
	}

	q := database.Get()
	guilds, err := q.RetrieveGuilds(context.Background(), sql.RetrieveGuildsParams{
		Limit:  int32(pageSize),
		Offset: int32(pageSize) * (int32(page) - 1),
	})

	if len(guilds) == 0 {
		guilds = []sql.Guild{}
	}

	return ctx.JSON(guilds)
}

// CreateGuild godoc
// @Summary Create guild
// @Tags guild
// @Accept json
// @Produce json
// @Param guild body models.CreateGuildInput true "Guild details"
// @Success 201 {object} sql.Guild
// @Failure 400 {object} validation.ErrorResponse
// @Router /guilds [post]
func CreateGuild(ctx *fiber.Ctx) error {
	var (
		guild      sql.Guild
		guildInput models.CreateGuildInput
		err        error
		errResp    []validation.ErrorResponse
		validator  = validation.GetValidatorInstance()
		q          = database.Get()
	)

	err = ctx.BodyParser(&guildInput)
	if err != nil {
		return fmt.Errorf("error parsing request body: %v", err)
	}

	errResp = validator.Validate(guildInput)
	if len(errResp) > 0 {
		return ctx.Status(fiber.StatusBadRequest).JSON(errResp)
	}

	var avatar pgtype.Text
	if guildInput.Avatar != nil {
		avatar = pgtype.Text{String: *guildInput.Avatar, Valid: true}
	} else {
		avatar = pgtype.Text{Valid: false}
	}

	var banner pgtype.Text
	if guildInput.Banner != nil {
		banner = pgtype.Text{String: *guildInput.Banner, Valid: true}
	} else {
		banner = pgtype.Text{Valid: false}
	}

	guild, err = q.CreateGuild(context.Background(), sql.CreateGuildParams{
		Name:   guild.Name,
		Avatar: avatar,
		Banner: banner,
	})
	if err != nil {
		log.Error(err)
		return ctx.Status(fiber.StatusInternalServerError).Send(make([]byte, 0))
	}

	return ctx.Status(fiber.StatusCreated).JSON(guild)
}
