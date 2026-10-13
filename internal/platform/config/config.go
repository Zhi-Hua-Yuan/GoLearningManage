package config

import (
	"fmt"
	"os"
	"strconv"
	"time"
)

type Config struct {
	HTTPAddr        string
	ContextPath     string
	Environment     string
	MySQLDSN        string
	JWTSecret       string
	ShutdownTimeout time.Duration
}

func Load() (Config, error) {
	shutdownTimeout, err := durationEnv("SHUTDOWN_TIMEOUT", 10*time.Second)
	if err != nil {
		return Config{}, err
	}

	return Config{
		HTTPAddr:        envOrDefault("HTTP_ADDR", ":8123"),
		ContextPath:     "/api",
		Environment:     envOrDefault("APP_ENV", "dev"),
		MySQLDSN:        os.Getenv("MYSQL_DSN"),
		JWTSecret:       os.Getenv("JWT_SECRET"),
		ShutdownTimeout: shutdownTimeout,
	}, nil
}

func envOrDefault(key, fallback string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return fallback
}

func durationEnv(key string, fallback time.Duration) (time.Duration, error) {
	value := os.Getenv(key)
	if value == "" {
		return fallback, nil
	}
	seconds, err := strconv.Atoi(value)
	if err != nil || seconds <= 0 {
		return 0, fmt.Errorf("%s must be a positive number of seconds", key)
	}
	return time.Duration(seconds) * time.Second, nil
}
