package config_test

import (
	"testing"
	"time"

	"github.com/Zhi-Hua-Yuan/GoLearningManage/internal/platform/config"
)

func TestLoadDefaults(t *testing.T) {
	for _, key := range []string{"HTTP_ADDR", "APP_ENV", "MYSQL_DSN", "JWT_SECRET", "SHUTDOWN_TIMEOUT"} {
		t.Setenv(key, "")
	}

	got, err := config.Load()
	if err != nil {
		t.Fatalf("Load() error = %v", err)
	}
	if got.HTTPAddr != ":8123" || got.ContextPath != "/api" || got.Environment != "dev" {
		t.Fatalf("defaults = %+v", got)
	}
	if got.ShutdownTimeout != 10*time.Second {
		t.Fatalf("ShutdownTimeout = %s, want 10s", got.ShutdownTimeout)
	}
}

func TestLoadRejectsInvalidShutdownTimeout(t *testing.T) {
	t.Setenv("SHUTDOWN_TIMEOUT", "not-a-number")
	if _, err := config.Load(); err == nil {
		t.Fatal("Load() error = nil, want validation error")
	}
}
