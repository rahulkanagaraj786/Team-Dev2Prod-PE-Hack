# Dev2Prod Client

The client is a Vite + React shell for the reliability cockpit.

## Local development

```bash
npm install
npm run dev
```

By default the Vite dev server proxies `/api/*` to `http://127.0.0.1:8000`, which matches the local control-plane entrypoint.

To point the client at a hosted control plane instead, set:

```bash
VITE_CONTROL_PLANE_URL=https://your-control-plane.example.com
```
