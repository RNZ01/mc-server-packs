# Minecraft resource pack drop folder

Drop `.zip` resource packs here and push to `main`.

Packs are merged in filename order; later files override earlier ones, matching Minecraft's stacked resource-pack priority. Use prefixes when order matters:

```text
01-base.zip
02-overrides.zip
```

The workflow publishes `Combined-Enchantments-26.2.zip` to the `26.2` GitHub release and writes the server.properties lines in the release notes.
