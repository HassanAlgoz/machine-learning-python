# Presentations (RevealJS)

Quarto supports creating RevealJS presentations with rich features.

## Speaker Notes

Speaker notes are hidden content that only appears in the speaker view.

### Syntax

Use a div with the class `.notes`.

```markdown
## Slide Title

- Point 1
- Point 2

::: {.notes}
These are the speaker notes for this slide.
They will not appear on the main screen.

- Reminder: Emphasize point 1.
- Joke: Why did the chicken cross the road?
:::
```

### Accessing Speaker View

Press `s` on your keyboard while viewing the presentation in a browser to open the speaker view.

## Fragments (Incremental Reveal)

Make content appear incrementally using the `.fragment` class.

```markdown
::: {.fragment}
Fade in
:::

::: {.fragment .fade-out}
Fade out
:::

::: {.fragment .highlight-red}
Highlight red
:::
```

## Columns

Arrange content side-by-side.

```markdown
::: {.columns}

::: {.column width="40%"}
Left column content.
:::

::: {.column width="60%"}
Right column content.
:::

:::
```

## Slide Backgrounds

Set background for a specific slide.

```markdown
## Slide with Background {background-color="aquamarine"}

## Slide with Image {background-image="image.png" background-size="contain"}
```
