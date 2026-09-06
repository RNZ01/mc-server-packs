# Minecraft resource pack drop folder

Drop `.zip` resource packs here and push to `main`.

Packs are merged in filename order; later files override earlier ones, matching Minecraft's stacked resource-pack priority. Use prefixes when order matters:

```text
01-base.zip
02-overrides.zip
```

The workflow publishes `Combined-Packs-26.2-0.N.zip` to a new `26.2-0.N` GitHub release each time and writes the server.properties lines in the release notes.
