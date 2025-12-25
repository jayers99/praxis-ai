# Create Domain Opinions

When `praxis.yaml` has `domain: create`, load this file into context.

## Foundational Principles

<!-- TODO: Create principles.md for the create domain covering foundational creative principles -->

See [principles.md](principles.md) for the foundational creative principles that guide all create domain work.

## Available Opinions

| Opinion                           | Triggers                                                                                                                                                       | Summary                                                                                            |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| [style-catalog](style-catalog.md) | style, visual, aesthetic, typography, font, color, palette, brand, design system, spacing, hierarchy, contrast, mood, tone, minimalist, handcrafted, brutalist | Style Catalog: A collection of reusable visual and aesthetic patterns serving content and audience |
| [materials](materials.md)         | material, medium, physical, tangible, paper, canvas, fabric, wood, metal, print, substrate, texture, finish, production                                        | Creative materials: intentional selection based on purpose, durability, practical constraints      |

## How This Works

1. This README is loaded when domain = create
2. If conversation matches any **trigger** keywords, load **all** matching detail files
3. If a file extends another, load the base file too
4. Apply all loaded opinions to your reasoning and suggestions

Multiple opinions can apply simultaneously. Base opinions provide general best practices; extended opinions add specific tooling and patterns.

## Maintenance

When an opinion file changes, ask AI to regenerate its row in the table above. AI will read the detail file and extract updated triggers and summary.
