// AlphaX Floor — embedded floor-plan designer.
// Upload a Floor Plan Image, then drag the tables of this floor to set X/Y.
// Positions auto-save on drop via alphax_pos.alphax_pos.api.floorplan.save_position

const STAGE_W = 900;
const STAGE_H = 520;
const GRID = 8;
const SIZE = 64;
const STATUS_COLORS = {
  free: "#1e9e6a",
  seated: "#d98c00",
  billed: "#2f6fb0",
  reserved: "#8a8f98",
};

frappe.ui.form.on("AlphaX Floor", {
  refresh(frm) {
    render_designer(frm);
  },
  floor_image(frm) {
    if (!frm.is_new()) render_designer(frm);
  },
});

async function render_designer(frm) {
  const field = frm.get_field("plan_html");
  if (!field) return;
  const $w = field.$wrapper;
  $w.empty();

  if (frm.is_new()) {
    $w.html(
      `<div class="text-muted" style="padding:16px">${__(
        "Save the floor first, then upload a Floor Plan Image and drag tables to position them."
      )}</div>`
    );
    return;
  }

  // Toolbar
  const $bar = $(
    `<div style="display:flex;gap:8px;align-items:center;margin-bottom:8px;flex-wrap:wrap">
       <button class="btn btn-xs btn-default axp-add">${__("+ Add Table")}</button>
       <button class="btn btn-xs btn-default axp-reload">${__("Reload")}</button>
       <span class="text-muted">${__("Drag tables to position. Saves automatically.")}</span>
       <span class="axp-msg" style="margin-left:auto;font-weight:600"></span>
     </div>`
  ).appendTo($w);

  // Stage
  const $stage = $(
    `<div class="axp-stage" style="position:relative;width:100%;max-width:${STAGE_W}px;
       height:${STAGE_H}px;border:1px solid var(--border-color);border-radius:10px;
       overflow:hidden;background:#f6f6f6;touch-action:none;"></div>`
  ).appendTo($w);

  if (frm.doc.floor_image) {
    $stage.css({
      "background-image": `url('${frm.doc.floor_image}')`,
      "background-size": "cover",
      "background-position": "center",
    });
  } else {
    $stage.css({
      "background-image":
        "linear-gradient(#0000000d 1px,transparent 1px),linear-gradient(90deg,#0000000d 1px,transparent 1px)",
      "background-size": "24px 24px",
    });
  }

  let tables = [];
  try {
    tables = await frappe.db.get_list("AlphaX Table", {
      filters: { floor: frm.doc.name },
      fields: ["name", "table_label", "x", "y", "shape", "status", "seats"],
      limit: 0,
    });
  } catch (e) {
    $stage.html(`<div style="padding:16px" class="text-danger">${__("Could not load tables.")}</div>`);
    return;
  }

  if (!tables.length) {
    $stage.append(
      `<div style="position:absolute;inset:0;display:grid;place-items:center;color:#999">
         ${__("No tables on this floor yet. Use “+ Add Table”.")}
       </div>`
    );
  }

  tables.forEach((t) => place_table(frm, $stage, t));

  $bar.find(".axp-add").on("click", () =>
    frappe.new_doc("AlphaX Table", { floor: frm.doc.name })
  );
  $bar.find(".axp-reload").on("click", () => render_designer(frm));
}

function place_table(frm, $stage, t) {
  const x = clamp(t.x || 16, 0, STAGE_W - SIZE);
  const y = clamp(t.y || 16, 0, STAGE_H - SIZE);
  const color = STATUS_COLORS[t.status] || STATUS_COLORS.free;
  const isRect = t.shape === "rect";
  const radius = t.shape === "circle" ? "50%" : "10px";
  const w = isRect ? SIZE * 1.6 : SIZE;

  const $t = $(
    `<div class="axp-table" data-name="${frappe.utils.escape_html(t.name)}"
       title="${frappe.utils.escape_html(t.status || "")}"
       style="position:absolute;left:${x}px;top:${y}px;width:${w}px;height:${SIZE}px;
       background:${color};color:#fff;border-radius:${radius};display:flex;flex-direction:column;
       align-items:center;justify-content:center;cursor:grab;font-size:12px;font-weight:600;
       box-shadow:0 2px 6px #00000033;user-select:none;touch-action:none;">
       <div>${frappe.utils.escape_html(t.table_label || t.name)}</div>
       <div style="font-weight:400;opacity:.9;font-size:11px">${__("{0} seats", [t.seats || 0])}</div>
     </div>`
  ).appendTo($stage);

  make_draggable($t[0], $stage, frm);
}

function make_draggable(el, $stage, frm) {
  let sx = 0, sy = 0, ox = 0, oy = 0, dragging = false, pid = null;

  el.addEventListener("pointerdown", (e) => {
    dragging = true;
    pid = e.pointerId;
    try { el.setPointerCapture(pid); } catch (_) {}
    el.style.cursor = "grabbing";
    sx = e.clientX; sy = e.clientY;
    ox = parseInt(el.style.left) || 0;
    oy = parseInt(el.style.top) || 0;
    e.preventDefault();
  });

  el.addEventListener("pointermove", (e) => {
    if (!dragging) return;
    const maxX = $stage.width() - el.offsetWidth;
    const maxY = $stage.height() - el.offsetHeight;
    let nx = clamp(ox + (e.clientX - sx), 0, maxX);
    let ny = clamp(oy + (e.clientY - sy), 0, maxY);
    nx = Math.round(nx / GRID) * GRID;
    ny = Math.round(ny / GRID) * GRID;
    el.style.left = nx + "px";
    el.style.top = ny + "px";
  });

  const end = async () => {
    if (!dragging) return;
    dragging = false;
    el.style.cursor = "grab";
    if (pid != null) { try { el.releasePointerCapture(pid); } catch (_) {} pid = null; }
    const name = el.dataset.name;
    const x = parseInt(el.style.left) || 0;
    const y = parseInt(el.style.top) || 0;
    try {
      await frappe.call({
        method: "alphax_pos.alphax_pos.api.floorplan.save_position",
        args: { table: name, x, y },
      });
      flash($stage, __("Saved {0}", [name]), "var(--text-on-green, #1e9e6a)");
    } catch (e) {
      flash($stage, __("Save failed"), "#c0392b");
    }
  };

  el.addEventListener("pointerup", end);
  el.addEventListener("pointercancel", end);
}

function flash($stage, text, color) {
  const $msg = $stage.closest(".form-group, .frappe-control").find(".axp-msg");
  const $m = $msg.length ? $msg : $(".axp-msg");
  $m.css("color", color || "#1e9e6a").text(text);
  setTimeout(() => $m.text(""), 1800);
}

function clamp(v, lo, hi) {
  return Math.max(lo, Math.min(v, hi));
}
