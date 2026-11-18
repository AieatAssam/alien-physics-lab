import { loadReplay } from "../data";
import { mountReplay, type ReplayHandle } from "../replay";
import { esc, labHref, labName, message, type Cleanup, type Route } from "../util";

export async function render(el: HTMLElement, route: Route): Promise<Cleanup | void> {
  const rid = route.params.join("/");
  if (!rid) {
    el.innerHTML = message("replay", "no request id given.");
    return;
  }
  const data = await loadReplay(rid);
  if (!data) {
    el.innerHTML = message("replay", `no published replay for ${rid}.`);
    return;
  }
  el.innerHTML = `<div class="container">
    <header class="page-head">
      <h1 class="display-s">${esc(data.purpose || "experiment")}</h1>
      <div class="page-head__meta">
        <span class="mono">${esc(data.request_id)}</span>
        ${data.lab ? `<a class="link" href="${labHref(data.lab)}">${esc(labName(data.lab))}</a>` : ""}
      </div>
    </header>
    <div data-host class="replay--wide"></div>
  </div>`;
  const host = el.querySelector<HTMLElement>("[data-host]")!;
  const handle: ReplayHandle = mountReplay(host, data, {
    label: data.purpose,
    overlay: false,
    autoplay: true,
  });
  return () => handle.destroy();
}
