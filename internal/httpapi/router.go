package httpapi

import (
	"github.com/Zhi-Hua-Yuan/GoLearningManage/internal/health"
	"github.com/Zhi-Hua-Yuan/GoLearningManage/internal/platform/trace"
	"github.com/gin-gonic/gin"
)

func NewRouter() *gin.Engine {
	gin.SetMode(gin.ReleaseMode)
	router := gin.New()
	router.Use(gin.Recovery(), trace.Middleware())

	api := router.Group("/api")
	api.GET("/health", health.Handler)

	return router
}
