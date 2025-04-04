#!/bin/bash

ollama serve &
sleep 5
ollama pull $MODEL_NAME
wait $!
