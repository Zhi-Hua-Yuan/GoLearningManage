package trace

import (
	"crypto/rand"
	"encoding/hex"
	"fmt"
	"regexp"
	"sync/atomic"
	"time"

	"github.com/gin-gonic/gin"
)

const Header = "X-Trace-Id"

var validTraceID = regexp.MustCompile(`^[0-9a-f]{32}$`)
var fallbackCounter uint64

func Middleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		traceID := c.GetHeader(Header)
		if !validTraceID.MatchString(traceID) {
			traceID = newTraceID()
		}
		c.Set(Header, traceID)
		c.Header(Header, traceID)
		c.Next()
		c.Header(Header, traceID)
	}
}

func newTraceID() string {
	var raw [16]byte
	if _, err := rand.Read(raw[:]); err == nil {
		return hex.EncodeToString(raw[:])
	}
	return fmt.Sprintf("%016x%016x", time.Now().UnixNano(), atomic.AddUint64(&fallbackCounter, 1))
}

func IsValid(value string) bool {
	return validTraceID.MatchString(value)
}
