# Data to Discovery portable portfolio metadata contract v1

`data-to-discovery/1.0` is an authoring contract for public scientific-resource
apps. A resource publishes a manifest that a future Data to Discovery portal can
consume. It is deliberately separate from a resource's Streamlit catalogue,
local routing, session state, card presentation, and learner pedagogy.

The Starter is authoring infrastructure only. It does not publish a manifest
for Template Experience, Data Playground, Pattern Reference, or any other
Starter surface. Synthetic fixtures in `tests/fixtures/portfolio_metadata/`
exercise the contract; they are not real resource manifests or curriculum
mappings.

## Manifest shape

Manifests are JSON documents with this top-level shape:

```json
{
  "schema_version": "data-to-discovery/1.0",
  "resource": {},
  "experiences": []
}
```

## Required resource metadata

```json
{
  "resource_id": "animal-traits",
  "title": "Animal Traits Data Science",
  "summary": "A classroom-ready resource for learning with authentic animal-trait data.",
  "repository": "https://github.com/example/animal-traits",
  "app_url": "https://example.org/animal-traits"
}
```

All resource fields are required and nonblank. `resource_id` is lowercase
kebab case; `repository` and `app_url` are structurally valid HTTPS URLs.

## Required experience metadata

```json
{
  "experience_id": "animal-traits/mice-to-elephants-and-beyond",
  "title": "Mice to Elephants: And Beyond",
  "summary": "A guided investigation using animal-trait data.",
  "kind": "guided_experience",
  "published": true,
  "stages": ["Stage 4"],
  "duration_minutes": {"minimum": 90, "maximum": 120},
  "science_focus": ["animal-traits", "comparative-biology"],
  "data_science_focus": ["modelling", "prediction"],
  "curriculum": [],
  "umbrellas": ["wild-data"],
  "delivery_modes": ["classroom"],
  "programmes": [],
  "evidence_types": ["curated_dataset", "derived_model"],
  "launch": {"url": "https://example.org/animal-traits/mice-to-elephants-and-beyond"}
}
```

Every field above must be present. The following empty or null values are
valid where no truthful claim applies:

- `stages`, `curriculum`, `umbrellas`, `delivery_modes`, and `programmes` may
  be empty lists.
- `duration_minutes` may be `null` for genuinely unbounded or not responsibly
  estimable exploration.
- `launch` must be an HTTPS URL object when `published` is `true`, and must be
  `null` when `published` is `false`.

`science_focus`, `data_science_focus`, and `evidence_types` must be nonempty.

## Stable IDs and local boundaries

`resource_id` is a globally unique lowercase-kebab identifier.
`experience_id` must be `{resource_id}/{experience-slug}`, where the slug is
also lowercase kebab case. Both identifiers remain stable when a title,
thumbnail, hosting provider, Streamlit route, local route name, or pathway
changes.

The portable contract never contains local fields such as `name`, `label`,
`nav_label`, `card_title`, `card_summary`, `icon`, `app_experience`, or
`pathway`. This allows several public experiences to retain distinct stable IDs
while sharing one local Streamlit route and different internal pathways.

## Controlled values

### Kinds

- `guided_experience`
- `explore_resource`

### Stages

- `Early Stage 1`
- `Stage 1` through `Stage 6`

Stage ordering has no semantic meaning. Validation checks only allowed values
and uniqueness. Historical local labels such as Year 8 and Year 10 are not
portable metadata.

### Delivery modes and programmes

Delivery modes are `facilitated`, `classroom`, and `independent`.
Programmes use stable uppercase tokens such as `CURIOUS`; they are distinct
from both delivery mode and stage.

### Evidence types

- `observational_measurements`
- `scientific_catalogue`
- `curated_dataset`
- `derived_model`
- `simulation`
- `external_reference_data`
- `citizen_science`

Science and data-science focus values are lowercase kebab-case tokens. V1
validates syntax only. A deliberately governed shared focus registry can be
added later without making a large speculative taxonomy part of this contract.

## Duration and curriculum

When known, `duration_minutes` is exactly:

```json
{"minimum": 15, "maximum": 45}
```

Both values are positive integers and `minimum` cannot exceed `maximum`.

`curriculum` is a list of frameworks and supports NESA outcome-level and
project detailed-content-level alignment:

```json
[
  {
    "framework": "nsw-science-7-10",
    "outcomes": [
      {
        "outcome_code": "SC4-DA1-01",
        "alignment": "DIRECT",
        "detailed_content": [
          {"content_id": "SC4-DA1-01.M2", "alignment": "DIRECT"}
        ]
      }
    ]
  }
]
```

Alignment values are `DIRECT`, `PARTIAL`, `POTENTIAL`, and `NOT_ADDRESSED`.
The validator checks required structure, NESA-style outcome-code syntax, and
that each detailed-content ID begins with its parent outcome code. It does not
judge pedagogical truth. This repository has no canonical versioned NESA
registry, so registry membership validation is deliberately deferred to later
shared infrastructure.

## Global umbrellas

`umbrellas` is a list of global portfolio collection tokens, never
resource-scoped IDs. Public collection titles are held in the shared portfolio
registry so resources do not repeat them inconsistently. V1 registers:

```text
wild-data -> Wild Data
```

Use `[]` when no umbrella applies. The Starter does not assign any of its local
experiences to `wild-data` or another umbrella.

## Launches, thumbnails, and relationships

`launch.url` is an opaque, public HTTPS canonical experience URL. It must open
the public experience without exposing Streamlit session-state or route
internals. A hosting change may update the URL but must not change the stable
experience ID. Streamlit sleep/wake behaviour, URL fetchability, redirects,
and network availability are operational health checks, not schema validity.
The validator makes no network requests.

`thumbnail` is optional:

```json
{
  "url": "https://example.org/assets/experience-card.png",
  "alt": "A concise meaningful image description",
  "caption": "Optional attribution or context."
}
```

The URL may use the deployed resource, GitHub/raw GitHub, or another stable
public source. `alt` is required when a thumbnail is supplied; `caption` is
optional or `null`.

`relationships` is optional and intentionally advisory:

```json
{
  "pairs_with": ["animal-traits/data-exploration-playground"],
  "suggested_after": ["animal-traits/mice-to-elephants-and-beyond"]
}
```

`suggested_after` means the current experience is suggested after the listed
experience. Local validation checks reference syntax, duplicates, and
self-reference only. Cross-manifest target resolution belongs to later
portfolio-level validation and health checking.

## Offline validator

Use the standard-library validator against a JSON manifest:

```bash
python -c "from tools.portfolio_metadata_validator import load_manifest, validate_manifest; print(validate_manifest(load_manifest('manifest.json')))"
```

It validates structure only; it never performs network access and it does not
publish a manifest.
