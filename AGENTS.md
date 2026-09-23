# Project Instructions

This project is prepared for AI-assisted app design and development with Codex and Agent Skills.

## Primary Goals

- Explore product ideas with AI
- Complete product.md through AI interview
- Generate multiple Android-feasible UI/UX directions
- Create prototype only after UX direction is selected
- Produce Android Jetpack Compose implementation spec before coding

## Important Rules

Codex should not write production Android code immediately.

The recommended workflow is:

1. Complete docs/product.md
2. Generate UI/UX directions
3. Select one direction
4. Create prototype or wireframe
5. Convert design into Android implementation spec
6. Implement with Jetpack Compose

## Design Requirements

- Prefer Android Material 3
- Prefer practical Android implementation
- Avoid web-only effects that are hard to implement on Android
- Clearly separate UX decisions, visual design, and implementation details
- Always mention which parts are native Material 3 and which require custom Compose components

## Useful Skills

- Use web-design-engineer for UI/UX, landing page, prototypes, design systems
- Use gpt-image-2 for app icon, hero image, illustration, visual asset prompts
- Use kb-retriever when reading local product documents

## Project Documents

- docs/product.md: Product specification draft and final product source of truth
- docs/prompts/01-complete-product-md.md: First prompt to complete product.md
- docs/prompts/02-ui-ux-directions.md: Prompt to generate UI/UX directions
