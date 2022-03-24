#!/bin/bash
uvicorn main:app --host 0.0.0.0 --reload --log-config logger_config.yaml