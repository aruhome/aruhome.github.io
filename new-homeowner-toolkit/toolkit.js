(function () {
    var STORAGE_KEY = "aruhome-new-homeowner-checklist-v1";
    var CANONICAL = "https://aruhome.github.io/new-homeowner-toolkit/";

    var boxes = Array.prototype.slice.call(document.querySelectorAll(".tk-task input[type='checkbox']"));
    var live = document.getElementById("checklist-live");
    var storageNote = document.getElementById("storage-note");
    var shareStatus = document.getElementById("share-status");
    var refNote = document.getElementById("ref-note");
    var resetDialog = document.getElementById("reset-dialog");
    var canStore = true;

    function safeRef() {
        var params;
        try {
            params = new URLSearchParams(window.location.search);
        } catch (err) {
            return "";
        }
        var ref = params.get("ref") || "";
        return /^[A-Za-z0-9_-]{1,40}$/.test(ref) ? ref : "";
    }

    function shareUrl() {
        var ref = safeRef();
        return ref ? CANONICAL + "?ref=" + encodeURIComponent(ref) : CANONICAL;
    }

    function readStored() {
        try {
            var raw = window.localStorage.getItem(STORAGE_KEY);
            if (!raw) return [];
            var parsed = JSON.parse(raw);
            return Array.isArray(parsed) ? parsed : [];
        } catch (err) {
            canStore = false;
            return [];
        }
    }

    function writeStored() {
        if (!canStore) return;
        var ids = boxes.filter(function (box) { return box.checked; }).map(function (box) { return box.id; });
        try {
            window.localStorage.setItem(STORAGE_KEY, JSON.stringify(ids));
        } catch (err) {
            canStore = false;
            if (storageNote) {
                storageNote.textContent = "This browser did not save the checklist. You can still check items during this visit. Nothing is sent to AruHome.";
            }
        }
    }

    function updateGroup(group) {
        var groupBoxes = boxes.filter(function (box) { return box.getAttribute("data-group") === group; });
        var done = groupBoxes.filter(function (box) { return box.checked; }).length;
        var count = document.querySelector('[data-count="' + group + '"]');
        var bar = document.querySelector('[data-bar="' + group + '"]');
        if (count) count.textContent = done + " of " + groupBoxes.length;
        if (bar) bar.style.width = (groupBoxes.length ? (done / groupBoxes.length) * 100 : 0) + "%";
    }

    function updateAll() {
        var done = boxes.filter(function (box) { return box.checked; }).length;
        ["day", "week", "month", "quarter"].forEach(updateGroup);
        var overall = document.getElementById("overall-count");
        var overallBar = document.querySelector('[data-bar="overall"]');
        if (overall) overall.textContent = done + " of " + boxes.length + " tasks checked";
        if (overallBar) overallBar.style.width = (boxes.length ? (done / boxes.length) * 100 : 0) + "%";
        var meter = document.getElementById("overall-meter");
        if (meter) {
            meter.setAttribute("aria-valuenow", String(done));
            meter.setAttribute("aria-valuemax", String(boxes.length));
        }
        if (live) live.textContent = done + " of " + boxes.length + " move-in tasks checked.";
    }

    var saved = readStored();
    boxes.forEach(function (box) {
        box.checked = saved.indexOf(box.id) !== -1;
        box.addEventListener("change", function () {
            writeStored();
            updateAll();
        });
    });
    updateAll();

    if (!canStore && storageNote) {
        storageNote.textContent = "Checklist progress stays in this browser only when storage is available. Nothing is uploaded.";
    }

    var ref = safeRef();
    if (ref && refNote) {
        refNote.hidden = false;
        refNote.textContent = "This link includes a share code. The code stays in the address bar so it can be passed along. Checklist progress is not sent with it.";
    }

    var resetOpen = document.getElementById("reset-open");
    if (resetOpen && resetDialog && typeof resetDialog.showModal === "function") {
        resetOpen.addEventListener("click", function () { resetDialog.showModal(); });
        resetDialog.addEventListener("close", function () {
            if (resetDialog.returnValue !== "reset") return;
            boxes.forEach(function (box) { box.checked = false; });
            writeStored();
            updateAll();
        });
    } else if (resetOpen) {
        resetOpen.addEventListener("click", function () {
            if (!window.confirm("Clear every checked task in this browser?")) return;
            boxes.forEach(function (box) { box.checked = false; });
            writeStored();
            updateAll();
        });
    }

    function setStatus(message) {
        if (shareStatus) shareStatus.textContent = message;
    }

    var copyBtn = document.getElementById("copy-link");
    if (copyBtn) {
        copyBtn.addEventListener("click", function () {
            var url = shareUrl();
            function fallback() {
                var field = document.createElement("textarea");
                field.value = url;
                field.setAttribute("readonly", "");
                field.style.position = "fixed";
                field.style.left = "-999px";
                document.body.appendChild(field);
                field.select();
                var ok = false;
                try { ok = document.execCommand("copy"); } catch (err) { ok = false; }
                document.body.removeChild(field);
                setStatus(ok ? "Link copied." : "Copy this link: " + url);
            }
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(url).then(function () {
                    setStatus("Link copied.");
                }).catch(fallback);
            } else {
                fallback();
            }
        });
    }

    var shareBtn = document.getElementById("native-share");
    if (shareBtn) {
        if (!navigator.share) shareBtn.hidden = true;
        shareBtn.addEventListener("click", function () {
            navigator.share({
                title: "New Homeowner Toolkit",
                text: "A free guide for settling in, organizing home records, and planning maintenance.",
                url: shareUrl()
            }).then(function () {
                setStatus("Share sheet opened.");
            }).catch(function (err) {
                if (err && err.name === "AbortError") return;
                setStatus("Sharing is not available in this browser. Use Copy link instead.");
            });
        });
    }

    var mail = document.getElementById("email-share");
    if (mail) {
        var subject = encodeURIComponent("New homeowner toolkit");
        var body = encodeURIComponent("A free guide for organizing a new home and planning maintenance:\n" + shareUrl());
        mail.href = "mailto:?subject=" + subject + "&body=" + body;
    }

    function printTarget(id) {
        var node = document.getElementById(id);
        if (!node) return;
        node.classList.add("is-print-target");
        document.body.classList.add("is-partial-print");
        window.print();
    }

    window.addEventListener("afterprint", function () {
        document.body.classList.remove("is-partial-print");
        document.querySelectorAll(".is-print-target").forEach(function (node) {
            node.classList.remove("is-print-target");
        });
    });

    document.querySelectorAll("[data-print]").forEach(function (button) {
        button.addEventListener("click", function () {
            var id = button.getAttribute("data-print");
            if (id === "all") {
                window.print();
                return;
            }
            printTarget(id);
        });
    });
})();
