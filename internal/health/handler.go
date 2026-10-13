package health

import (
	"net/http"

	"github.com/Zhi-Hua-Yuan/GoLearningManage/internal/common"
	"github.com/gin-gonic/gin"
)

func Handler(c *gin.Context) {
	c.JSON(http.StatusOK, common.Success("ok"))
}
