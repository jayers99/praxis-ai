# Prompt Taxonomy (Create Domain)

This doc defines the **building blocks** for image generation prompts in Create projects, independent of any provider (DALL·E, Gemini/Imagen, SD, etc.).

The intent is:

- Create projects own *what* we want (prompts, reference bundles, variants).
- Code-domain utilities (e.g., Render Run) own *how* we execute (fan-out to providers + manifest + artifacts).

---

## Reference Bundles

Most real prompts need multiple reference classes:

1. **Likeness references (person)**
   - Goal: approximate a real person’s look.
   - Inputs: 1–6 photos with varied angles/lighting.
   - Notes: strict privacy + consent; avoid sensitive biometrics.

2. **Style references (aesthetic)**
   - Goal: replicate a look/medium (handcrafted, minimalist, watercolor, etc.).
   - Inputs: 1–3 images capturing palette, line quality, texture.
   - Notes: prefer “style direction” over copying a specific artist.

3. **Object references (anchors)**
   - Goal: force specific recognizable objects (apron, towels, bottle label style, etc.).
   - Inputs: close-up photos of the object.
   - Notes: best used as “must include” anchors.

---

## Prompt Building Blocks (Slots)

Think of a prompt as a composition of slots. Some are required for control, some are optional.

### Required (for decent control)

- **Subject**: who/what is the focal point.
- **Action / pose**: what the subject is doing.
- **Setting**: where it happens.
- **Key anchors**: 1–4 “must include” details.
- **Mood / tone**: emotional direction.
- **Style / medium**: photo-real, illustration, handmade, etc.

### Optional (for more control)

- **Camera**: lens, distance, perspective.
- **Lighting**: time of day, soft/hard, indoor/outdoor.
- **Palette**: 2–4 color anchors.
- **Composition**: rule-of-thirds, centered portrait, negative space.
- **Constraints / exclusions**: negative prompt (no text, no watermarks, no extra limbs).
- **Output format**: aspect ratio, orientation (landscape/portrait/square), size.

---

## Prompt Specificity Spectrum

We use a 3-tier model:

- **Loose**: “Here’s the idea, surprise me.”
- **Balanced**: “Here are the anchors, make good composition choices.”
- **Strict**: “Place X in Y position, use Z palette, do not deviate.”

A Create project should decide which tier is appropriate **per variant**, not globally.

---

## Variations (How We Explore)

We explore by varying one axis at a time:

- **Style axis**: minimalist vs handcrafted vs cinematic photo.
- **Mood axis**: funny vs sentimental vs epic.
- **Composition axis**: close-up vs wide.
- **Constraint axis**: loose → strict.

Recommended starting set per idea:

- 3 variants (1 loose, 1 balanced, 1 strict)
- 2 providers
- 1–2 images per variant/provider

---

## Proposed Payload Template (Provider-Agnostic)

This is the “Create → Render Run” payload shape we want to converge on (can be serialized as YAML/JSON).

```yaml
item:
  title: "Joe — Padres towel mountain"
  idea: "A Padres apron + a mountain of striped dish towels behind him"
  prompt_slots:
    subject: "Joe"
    action: "standing proudly, playful grin"
    setting: "San Diego kitchen"
    mood: "funny, warm"
    style: "photo-real"
    camera: "35mm, eye-level"
    lighting: "soft indoor daylight"
    palette: "Padres navy and gold"
  reference_assets:
    likeness:
      - people/joe/joe-01.jpg
    style:
      - styles/minimalist-01.png
    objects:
      - objects/padres-apron.png
      - objects/striped-towels.png
  variants:
    - id: "1a"
      specificity_level: balanced
      must_include:
        - "Padres apron (navy/gold)"
        - "striped dish towels in a pile"
      avoid:
        - "text overlays"
        - "watermarks"
      params:
        aspect_ratio: "1:1"
        orientation: "square"
        size: "1024x1024"
        n: 2
```

Render Run should treat this payload as data (not opinions): it records it, expands it, executes it, and saves artifacts.
