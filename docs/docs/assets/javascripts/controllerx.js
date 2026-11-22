/*
 * ControllerX documentation helpers:
 * - Filters for the supported controllers catalogue (controllers/index.md)
 * - Configuration builder (start/config-builder.md)
 *
 * Both use `document$` so they work with `navigation.instant`.
 */
(function () {
  "use strict";

  // Resolve devices.json relative to this script:
  // <site>/assets/javascripts/controllerx.js -> <site>/controllers/devices.json
  var SCRIPT_URL = document.currentScript ? document.currentScript.src : null;
  var DEVICES_URL = SCRIPT_URL
    ? new URL("../../controllers/devices.json", SCRIPT_URL).href
    : null;
  var catalogue = null;

  function loadCatalogue() {
    if (!catalogue) {
      catalogue = fetch(DEVICES_URL).then(function (response) {
        if (!response.ok) throw new Error("Could not load " + DEVICES_URL);
        return response.json();
      });
    }
    return catalogue;
  }

  function el(tag, attrs, children) {
    var node = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (key) {
      if (key === "text") node.textContent = attrs[key];
      else node.setAttribute(key, attrs[key]);
    });
    (children || []).forEach(function (child) {
      node.appendChild(child);
    });
    return node;
  }

  /* ---------------------------------------------------------------------- */
  /* Supported controllers filters                                          */
  /* ---------------------------------------------------------------------- */

  function initCatalogueFilters() {
    var filters = document.querySelector(".cx-filters");
    var table = document.querySelector(".cx-catalogue table");
    if (!filters || !table) return;

    var headers = Array.prototype.map.call(
      table.querySelectorAll("thead th"),
      function (th) {
        return th.textContent.trim();
      }
    );
    var rows = Array.prototype.slice.call(table.querySelectorAll("tbody tr"));
    var search = filters.querySelector(".cx-filter-search");
    var selects = Array.prototype.slice.call(
      filters.querySelectorAll("select.cx-filter")
    );
    var count = filters.querySelector(".cx-filter-count");

    function cellValues(row, column) {
      var cell = row.cells[headers.indexOf(column)];
      return cell
        ? cell.textContent.split(",").map(function (value) {
            return value.trim();
          })
        : [];
    }

    function apply() {
      var query = search.value.trim().toLowerCase();
      var visible = 0;
      rows.forEach(function (row) {
        var matches =
          row.textContent.toLowerCase().indexOf(query) !== -1 &&
          selects.every(function (select) {
            return (
              !select.value ||
              cellValues(row, select.dataset.column).indexOf(select.value) !== -1
            );
          });
        row.hidden = !matches;
        if (matches) visible++;
      });
      count.textContent = "Showing " + visible + " of " + rows.length + " devices";
    }

    search.addEventListener("input", apply);
    selects.forEach(function (select) {
      select.addEventListener("change", apply);
    });
    filters.hidden = false;
    apply();
  }

  /* ---------------------------------------------------------------------- */
  /* Configuration builder                                                  */
  /* ---------------------------------------------------------------------- */

  function yamlScalar(value) {
    var text = String(value);
    var needsQuotes =
      text === "" ||
      /^(on|off|yes|no|true|false|null|~)$/i.test(text) ||
      /^[\s\-?:,\[\]{}#&*!|>'"%@`]/.test(text) ||
      /:|#|\s$/.test(text);
    return needsQuotes ? '"' + text.replace(/\\/g, "\\\\").replace(/"/g, '\\"') + '"' : text;
  }

  function buildYaml(state) {
    var lines = [
      (state.appName || "my_controller_app") + ":",
      "  module: controllerx",
      "  class: " + state.type.class,
    ];
    var example = state.example;
    if (example.attrs) {
      lines.push("  integration:");
      lines.push("    name: " + example.name);
      Object.keys(example.attrs).forEach(function (key) {
        lines.push("    " + key + ": " + yamlScalar(example.attrs[key]));
      });
    } else {
      lines.push("  integration: " + example.name);
    }
    lines.push("  controller: " + yamlScalar(state.controller || example.controller));
    var entity =
      state.entity ||
      (state.type.domain ? state.type.domain + ".my_entity_id" : "my_entity_id");
    lines.push("  " + state.type.entity_arg + ": " + yamlScalar(entity));
    return lines.join("\n");
  }

  function field(label, input, help) {
    var children = [el("span", { class: "cx-builder-label", text: label }), input];
    if (help) children.push(help);
    return el("label", { class: "cx-builder-field" }, children);
  }

  function initBuilder() {
    var root = document.getElementById("cx-builder");
    if (!root || root.dataset.ready) return;
    root.dataset.ready = "true";
    root.textContent = "Loading devices…";

    loadCatalogue()
      .then(function (data) {
        renderBuilder(root, data);
      })
      .catch(function (error) {
        root.textContent =
          "The configuration builder could not be loaded (" + error.message + ").";
      });
  }

  function renderBuilder(root, data) {
    var siteRoot = new URL("../../", SCRIPT_URL).href;
    var params = new URLSearchParams(window.location.search);
    var devices = {};
    data.devices.forEach(function (device) {
      devices[device.id] = device;
    });

    // Device select grouped by manufacturer
    var deviceSelect = el("select", { "aria-label": "Device" });
    var groups = {};
    data.devices
      .slice()
      .sort(function (a, b) {
        return a.manufacturer.localeCompare(b.manufacturer) || a.id.localeCompare(b.id);
      })
      .forEach(function (device) {
        if (!groups[device.manufacturer]) {
          groups[device.manufacturer] = el("optgroup", { label: device.manufacturer });
          deviceSelect.appendChild(groups[device.manufacturer]);
        }
        groups[device.manufacturer].appendChild(
          el("option", { value: device.id, text: device.title })
        );
      });

    var typeSelect = el("select", { "aria-label": "Controller type" });
    var integrationSelect = el("select", { "aria-label": "Integration" });
    var appNameInput = el("input", {
      type: "text",
      class: "md-input",
      value: params.get("name") || "livingroom_controller",
      spellcheck: "false",
    });
    var controllerInput = el("input", { type: "text", class: "md-input", spellcheck: "false" });
    var controllerHelp = el("small", { class: "cx-builder-help" });
    var entityInput = el("input", { type: "text", class: "md-input", spellcheck: "false" });
    var entityField = field("Entity", entityInput);

    var code = el("code", {});
    var output = el("pre", { class: "cx-builder-output" }, [code]);
    var copyButton = el("button", {
      type: "button",
      class: "md-button md-button--primary",
      text: "Copy configuration",
    });
    var deviceLink = el("a", { class: "md-button", text: "See default mapping" });

    root.textContent = "";
    root.appendChild(
      el("div", { class: "cx-builder-form" }, [
        field("1. Device", deviceSelect),
        field("2. What do you want to control?", typeSelect),
        field("3. Integration", integrationSelect),
        field("4. App name", appNameInput),
        field("5. Controller ID", controllerInput, controllerHelp),
        entityField,
      ])
    );
    root.appendChild(output);
    root.appendChild(el("div", { class: "cx-builder-actions" }, [copyButton, deviceLink]));

    function currentDevice() {
      return devices[deviceSelect.value];
    }

    function currentType() {
      var device = currentDevice();
      return device.controller_types[typeSelect.selectedIndex] || device.controller_types[0];
    }

    function currentExample() {
      return data.integration_examples.filter(function (example) {
        return example.id === integrationSelect.value;
      })[0];
    }

    function fillTypes(preferred) {
      typeSelect.textContent = "";
      currentDevice().controller_types.forEach(function (type) {
        typeSelect.appendChild(
          el("option", { value: type.anchor, text: type.type + " (" + type.class + ")" })
        );
      });
      if (preferred) typeSelect.value = preferred;
      if (typeSelect.selectedIndex < 0) typeSelect.selectedIndex = 0;
    }

    function fillIntegrations(preferred) {
      var previous = preferred || integrationSelect.value;
      integrationSelect.textContent = "";
      data.integration_examples
        .filter(function (example) {
          return currentType().integrations.indexOf(example.name) !== -1;
        })
        .forEach(function (example) {
          integrationSelect.appendChild(
            el("option", { value: example.id, text: example.title })
          );
        });
      integrationSelect.value = previous;
      if (integrationSelect.selectedIndex < 0) integrationSelect.selectedIndex = 0;
    }

    function update() {
      var device = currentDevice();
      var type = currentType();
      var example = currentExample();
      var integration = data.integrations[example.name];

      controllerInput.placeholder = example.controller;
      controllerHelp.textContent = "";
      controllerHelp.appendChild(document.createTextNode(example.controller_help.replace(/`/g, "") + ". "));
      controllerHelp.appendChild(
        el("a", { href: siteRoot + integration.url, text: "How to find it" })
      );
      entityField.querySelector(".cx-builder-label").textContent =
        "6. Entity to control (" + type.entity_arg + ")";
      entityInput.placeholder = type.domain ? type.domain + ".livingroom" : "my_entity_id";
      deviceLink.href = siteRoot + device.url + "#" + type.anchor;

      code.textContent = buildYaml({
        appName: appNameInput.value.trim(),
        type: type,
        example: example,
        controller: controllerInput.value.trim(),
        entity: entityInput.value.trim(),
      });

      var query = new URLSearchParams({
        device: device.id,
        type: type.anchor,
        integration: example.id,
      });
      window.history.replaceState(null, "", "?" + query.toString() + window.location.hash);
    }

    deviceSelect.value = devices[params.get("device")] ? params.get("device") : "E1810";
    if (deviceSelect.selectedIndex < 0) deviceSelect.selectedIndex = 0;
    fillTypes(params.get("type"));
    fillIntegrations(params.get("integration") || "z2m-mqtt");

    deviceSelect.addEventListener("change", function () {
      fillTypes(typeSelect.value);
      fillIntegrations();
      update();
    });
    typeSelect.addEventListener("change", function () {
      fillIntegrations();
      update();
    });
    [integrationSelect].forEach(function (node) {
      node.addEventListener("change", update);
    });
    [appNameInput, controllerInput, entityInput].forEach(function (node) {
      node.addEventListener("input", update);
    });
    copyButton.addEventListener("click", function () {
      navigator.clipboard.writeText(code.textContent).then(function () {
        copyButton.textContent = "Copied!";
        setTimeout(function () {
          copyButton.textContent = "Copy configuration";
        }, 2000);
      });
    });

    update();
  }

  /* ---------------------------------------------------------------------- */
  /* Total downloads in the repository facts (next to version/stars/forks)   */
  /* ---------------------------------------------------------------------- */

  var DOWNLOADS_URL =
    "https://img.shields.io/github/downloads/xaviml/controllerx/controllerx.zip.json?displayAssetName=false";
  var DOWNLOADS_KEY = "cx-downloads";
  var downloads = null;

  // Same caching as the theme's own facts: once per browser session
  function loadDownloads() {
    if (!downloads) {
      var cached = null;
      try {
        cached = sessionStorage.getItem(DOWNLOADS_KEY);
      } catch (e) {}
      downloads = cached
        ? Promise.resolve(cached)
        : fetch(DOWNLOADS_URL)
            .then(function (response) {
              if (!response.ok) throw new Error("Could not load downloads");
              return response.json();
            })
            .then(function (data) {
              try {
                sessionStorage.setItem(DOWNLOADS_KEY, data.value);
              } catch (e) {}
              return data.value;
            })
            .catch(function () {
              return null;
            });
    }
    return downloads;
  }

  function addDownloadsFact(facts) {
    if (facts.querySelector(".md-source__fact--downloads")) return;
    loadDownloads().then(function (value) {
      if (!value || facts.querySelector(".md-source__fact--downloads")) return;
      facts.appendChild(
        el("li", {
          class: "md-source__fact md-source__fact--downloads",
          title: "Total downloads",
          text: value,
        })
      );
    });
  }

  // The theme renders the facts asynchronously, and again for the navigation
  // drawer on every instant navigation, so watch for them to appear
  function initDownloadsFacts() {
    document.querySelectorAll(".md-source__facts").forEach(addDownloadsFact);
    new MutationObserver(function (records) {
      records.forEach(function (record) {
        record.addedNodes.forEach(function (node) {
          if (node.nodeType !== 1) return;
          if (node.matches(".md-source__facts")) addDownloadsFact(node);
          else node.querySelectorAll(".md-source__facts").forEach(addDownloadsFact);
        });
      });
    }).observe(document.body, { childList: true, subtree: true });
  }

  initDownloadsFacts();

  function init() {
    initCatalogueFilters();
    initBuilder();
  }

  if (typeof document$ !== "undefined") {
    document$.subscribe(init);
  } else {
    document.addEventListener("DOMContentLoaded", init);
  }
})();
