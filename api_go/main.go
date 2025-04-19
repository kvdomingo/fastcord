package main

import (
	"fastcord/config"
	"fastcord/controllers"
	"fastcord/database"
	_ "fastcord/docs"
	"flag"
	"fmt"
	"github.com/gofiber/contrib/swagger"
	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
	"github.com/gofiber/fiber/v2/middleware/healthcheck"
	"github.com/gofiber/fiber/v2/middleware/helmet"
	"github.com/gofiber/fiber/v2/middleware/idempotency"
	"github.com/gofiber/fiber/v2/middleware/logger"
	"github.com/gofiber/fiber/v2/middleware/monitor"
	"github.com/gofiber/fiber/v2/middleware/recover"
	_ "github.com/joho/godotenv/autoload"
	"log"
	"time"
)

// @title Fastcord
// @version 0.1.0
// @contact.name KVD Studio
// @contact.url https://kvd.studio
// @contact.email hello@kvd.studio
// @host localhost:8000
// @BasePath /api
func main() {
	flag.Parse()

	err := database.NewPool()
	if err != nil {
		log.Fatalf("Unable to connect to database: %v\n", err)
	}
	defer database.ClosePool()

	app := fiber.New(
		fiber.Config{
			Prefork:           false,
			AppName:           "Time Machine",
			ServerHeader:      "Fastcord",
			StrictRouting:     true,
			EnablePrintRoutes: true,
		},
	)

	app.Use(recover.New())
	app.Use(logger.New())
	app.Use(cors.New(cors.Config{
		AllowOrigins:     "*",
		AllowMethods:     "*",
		AllowHeaders:     "*",
		AllowCredentials: false,
	}))
	app.Use(
		healthcheck.New(
			healthcheck.Config{
				LivenessEndpoint: "/api/live",
				LivenessProbe: func(c *fiber.Ctx) bool {
					return true
				},
				ReadinessEndpoint: "/api/ready",
				ReadinessProbe: func(c *fiber.Ctx) bool {
					return true
				},
			},
		),
	)
	app.Use(idempotency.New())
	app.Use(
		swagger.New(
			swagger.Config{
				BasePath: "/api",
				FilePath: "docs/swagger.json",
				Path:     "docs",
				Title:    "Fastcord API",
				CacheAge: 1,
			},
		),
	)
	app.Use(helmet.New(helmet.Config{
		XSSProtection:             "0",
		ContentTypeNosniff:        "nosniff",
		XFrameOptions:             "SAMEORIGIN",
		ReferrerPolicy:            "no-referrer",
		CrossOriginEmbedderPolicy: "require-corp",
		CrossOriginOpenerPolicy:   "same-origin",
		CrossOriginResourcePolicy: "cross-origin",
		XDownloadOptions:          "noopen",
		XPermittedCrossDomain:     "none",
	}))
	app.Get("/metrics", monitor.New(monitor.Config{
		Title:   "Fastcord Metrics",
		Refresh: 5 * time.Second,
		APIOnly: false,
	}))

	api := app.Group("/api")

	api.Get("/guilds", controllers.RetrieveGuilds)
	api.Post("/guilds", controllers.CreateGuild)

	log.Fatal(app.Listen(fmt.Sprintf(":%s", config.Port())))
}
