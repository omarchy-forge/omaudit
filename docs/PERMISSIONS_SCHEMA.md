# Omaudit permissions convention

Status: experimental, schema version 1.

Omaudit recognizes an optional `permissions` object in a plugin's
`manifest.json`. This is an Omaudit convention, not an official Omarchy field,
permission prompt, sandbox, or enforcement mechanism. Omarchy currently ignores
the object.

Each key is a capability emitted by `omaudit schema`. Its value contains a
plain-language `reason` and, when applicable, a bounded `scope` array:

```json
{
  "permissions": {
    "net.outbound": {
      "reason": "Fetch the weather forecast selected by the user.",
      "scope": ["api.open-meteo.com"]
    }
  }
}
```

Unknown keys are rejected by Omaudit. Declarations communicate intent; they do
not make a capability safe or prevent undeclared behavior.
