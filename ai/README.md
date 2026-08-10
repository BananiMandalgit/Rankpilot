# AI Services

The AI module is the future integration boundary for RankPilot provider support and AI-powered SEO/AEO features. This branch only contains the foundation needed for future team members to extend the module safely.

## Current Structure

- `ai/src/clients/` - typed client abstractions for future providers
- `ai/src/prompts/` - prompt templates and reusable prompt helpers
- `ai/src/services/` - service boundary that will orchestrate providers later

## Future Provider Integration

The module is prepared for later Gemini, Groq, and Ollama integrations, but no provider calls exist yet.

## Status

Actual AI, SEO, and AEO logic is not implemented yet. This package only defines the shape of the future service layer.