{
  "name": "{{PKG_NAME}}",
  "version": "{{VERSION}}",
  "description": "{{DESCRIPTION_EN}}",
  "license": "{{LICENSE}}",{{AUTHOR_LINE}}
  "type": "module",
  "main": "lib/index.mjs",
  "types": "lib/index.d.mts",
  "exports": {
    ".": { "types": "./lib/index.d.mts", "default": "./lib/index.mjs" },{{CLIENT_EXPORT}}
    "./package.json": "./package.json"
  },
  "files": [
    "lib/index.mjs",
    "lib/index.d.mts",{{CLIENT_FILE}}
    "cordis.patch.yml"
  ],
  "keywords": [
    "dsh-plugin",
    "deepseek-harness"
  ],{{REPO_LINE}}
  "dsh": {
    "bundle": {
      "patch": "./cordis.patch.yml"
    }{{DSH_CLIENT_BLOCK}}
  },
  "scripts": {
    "build": "tsdown --config tsdown.config.ts",
    "typecheck": "tsc -p tsconfig.json --noEmit",
    "verify": "pnpm typecheck && pnpm build",
    "pack": "pnpm pack"
  },
  "peerDependencies": {
    "@deepseek-ai/cordis": "^4.0.1"{{PEER_DEPS}}
  },
  "devDependencies": {
    "@deepseek-ai/cordis": "^4.0.1",{{DEV_DEPS}}
    "@types/node": "^22.10.0",{{DEV_REACT}}
    "tsdown": "^0.22.14",
    "typescript": "^5.6.0"
  }
}
