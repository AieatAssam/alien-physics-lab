# alien-physics-lab site

The public journal for the lab. It is a static Vite + TypeScript app that reads
JSON generated from the repository by `build_data.py`. It has no server and no UI framework.

## Local development

```sh
python site/fixtures/make_fixture.py /tmp/fx
python site/build_data.py --repo /tmp/fx --out site/public/data
cd site && npm run dev
```

The fixture repo is fake data for local development only. Never deploy or publish it.

## Build

```sh
python site/build_data.py --repo . --out site/public/data --repo-url https://github.com/<owner>/<repo>
cd site && npm install && npm run build
```

`npm run build` type-checks with `tsc --noEmit` and then runs `vite build` into `site/dist`.
The app uses hash routes and a relative base, so `dist/` can be served from any path.

## Layout

- `build_data.py`: reads the repo and writes `site/public/data/` (index, events, papers, labs, replays, reveal). It tolerates missing inputs and produces empty data for an empty repo.
- `fixtures/make_fixture.py`: writes a fake repo with three labs, papers in each status, replays, and scores.
- `src/main.ts`: hash router, chrome, and view loader.
- `src/data.ts`: typed JSON loaders.
- `src/replay.ts`: canvas replay component used on every view that shows an experiment.
- `src/views/`: one module per view.
- `src/styles/`: `tokens.css` and `base.css` (scaffolded), `species.css`, and `app.css`.
- `DESIGN.md`: the locked design contract.

`site/public/data/` is generated and git-ignored.
