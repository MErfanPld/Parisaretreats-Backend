document.addEventListener("DOMContentLoaded", function () {
  var placeholder = "https://placehold.co/1600x900/eeeeee/333333?text=Image+Unavailable";
  document.querySelectorAll("img").forEach(function (img) {
    if (!img.hasAttribute("loading")) img.setAttribute("loading", "lazy");
    img.addEventListener("error", function () {
      if (img.dataset.fallbackApplied === "1") return;
      img.dataset.fallbackApplied = "1";
      img.src = placeholder;
    });
  });
  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) entry.target.classList.add("in");
    });
  }, { threshold: 0.12 });
  document.querySelectorAll(".reveal").forEach(function (el) { observer.observe(el); });
  var priceInput = document.querySelector("#filterPrice");
  var locationSelect = document.querySelector("#filterLocation");
  var typeSelect = document.querySelector("#filterType");
  var priceValue = document.querySelector("#priceValue");
  function applyFilters() {
    var maxPrice = priceInput ? parseInt(priceInput.value || "0", 10) : Infinity;
    var location = locationSelect ? locationSelect.value : "";
    var type = typeSelect ? typeSelect.value : "";
    document.querySelectorAll(".tour-card").forEach(function (card) {
      var cPrice = parseInt(card.dataset.price || "0", 10);
      var cLocation = card.dataset.location || "";
      var cType = card.dataset.type || "";
      var okPrice = cPrice <= (isFinite(maxPrice) ? maxPrice : cPrice);
      var okLocation = !location || location === "all" || cLocation === location;
      var okType = !type || type === "all" || cType === type;
      card.style.display = (okPrice && okLocation && okType) ? "" : "none";
    });
    if (priceValue && priceInput) priceValue.textContent = "$" + priceInput.value;
  }
  [priceInput, locationSelect, typeSelect].forEach(function (el) {
    if (el) el.addEventListener("input", applyFilters);
  });
  applyFilters();
  var detailModal = document.getElementById("tourDetailModal");
  var datePicker = document.getElementById("datePicker");
  var authModal = document.getElementById("authModal");
  document.querySelectorAll("[data-action='view-details']").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var target = new bootstrap.Modal(detailModal);
      target.show();
    });
  });
  var selectDateBtn = document.getElementById("selectDateBtn");
  if (selectDateBtn && datePicker) {
    selectDateBtn.addEventListener("click", function () {
      datePicker.classList.remove("d-none");
      datePicker.focus();
    });
    datePicker.addEventListener("change", function () {
      if (datePicker.value) {
        var m = new bootstrap.Modal(authModal);
        m.show();
      }
    });
  }
  var loginForm = document.getElementById("loginForm");
  var registerForm = document.getElementById("registerForm");
  var dashboard = document.getElementById("dashboard");
  var authOnly = document.querySelectorAll(".auth-only");
  function setLoggedIn(state) {
    try { localStorage.setItem("loggedIn", state ? "1" : "0"); } catch (e) {}
    if (dashboard) dashboard.classList.toggle("d-none", !state);
    authOnly.forEach(function (el) { el.classList.toggle("d-none", !state); });
  }
  var loggedIn = false;
  try { loggedIn = localStorage.getItem("loggedIn") === "1"; } catch (e) {}
  setLoggedIn(loggedIn);
  if (loginForm) {
    loginForm.addEventListener("submit", function (e) {
      e.preventDefault();
      setLoggedIn(true);
      var modalEl = document.getElementById("authModal");
      if (modalEl) bootstrap.Modal.getInstance(modalEl)?.hide();
    });
  }
  if (registerForm) {
    registerForm.addEventListener("submit", function (e) {
      e.preventDefault();
      setLoggedIn(true);
      var modalEl = document.getElementById("authModal");
      if (modalEl) bootstrap.Modal.getInstance(modalEl)?.hide();
    });
  }
  var payButtons = document.querySelectorAll("[data-action='pay-now']");
  var paymentModal = document.getElementById("paymentModal");
  payButtons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      var m = new bootstrap.Modal(paymentModal);
      m.show();
    });
  });
  var paymentForm = document.getElementById("paymentForm");
  if (paymentForm) {
    paymentForm.addEventListener("submit", function (e) {
      e.preventDefault();
      var m = bootstrap.Modal.getInstance(paymentModal);
      var toast = document.getElementById("paymentToast");
      if (toast) new bootstrap.Toast(toast).show();
      if (m) m.hide();
    });
  }
  var contactForm = document.getElementById("contactForm");
  var contactToast = document.getElementById("contactToast");
  if (contactForm) {
    contactForm.addEventListener("submit", function (e) {
      e.preventDefault();
      if (contactToast) new bootstrap.Toast(contactToast).show();
      contactForm.reset();
    });
  }
  var langSelect = document.getElementById("langSelect");
  function setLang(l) {
    try { localStorage.setItem("lang", l); } catch (e) {}
    document.documentElement.setAttribute("lang", l || "en");
    if (langSelect) langSelect.value = l || "en";
  }
  var savedLang = "en";
  try { savedLang = localStorage.getItem("lang") || "en"; } catch (e) {}
  setLang(savedLang);
  if (langSelect) {
    langSelect.addEventListener("change", function () { setLang(langSelect.value); });
  }
  var cartCountEl = document.getElementById("cartCount");
  var cartCount = 0;
  try { cartCount = parseInt(localStorage.getItem("cartCount") || "0", 10); } catch (e) {}
  if (cartCountEl) cartCountEl.textContent = isNaN(cartCount) ? "0" : String(cartCount);
  var reviewsTrack = document.getElementById("reviewsTrack");
  var reviewsNext = document.getElementById("reviewsNext");
  var reviewsPrev = document.getElementById("reviewsPrev");
  function reviewsSlide(dir) {
    if (!reviewsTrack) return;
    var amount = Math.max(280, Math.floor(reviewsTrack.clientWidth * 0.8));
    reviewsTrack.scrollBy({ left: dir * amount, behavior: "smooth" });
  }
  if (reviewsNext) reviewsNext.addEventListener("click", function () { reviewsSlide(1); });
  if (reviewsPrev) reviewsPrev.addEventListener("click", function () { reviewsSlide(-1); });
  if (reviewsTrack) {
    setInterval(function () {
      var maxScroll = reviewsTrack.scrollWidth - reviewsTrack.clientWidth - 8;
      if (reviewsTrack.scrollLeft >= maxScroll) {
        reviewsTrack.scrollTo({ left: 0, behavior: "smooth" });
      } else {
        reviewsSlide(1);
      }
    }, 4000);
  }
  var selectDateBtnDetails = document.getElementById("selectDateBtnDetails");
  var dateOptionsPanel = document.getElementById("dateOptionsPanel");
  var dateSelect = document.getElementById("dateSelect");
  var timeSelect = document.getElementById("timeSelect");
  var confirmSelection = document.getElementById("confirmSelection");
  function checkAndPromptAuth() {
    if (!authModal) return;
    var dateOk = dateSelect && dateSelect.value;
    var timeOk = timeSelect && timeSelect.value;
    var confirmOk = confirmSelection && confirmSelection.checked;
    if (dateOk && timeOk && confirmOk) {
      var m = new bootstrap.Modal(authModal);
      m.show();
    }
  }
  if (selectDateBtnDetails) {
    selectDateBtnDetails.addEventListener("click", function () {
      checkAndPromptAuth();
    });
  }
  [dateSelect, timeSelect].forEach(function (el) {
    if (el) el.addEventListener("change", checkAndPromptAuth);
  });
  if (confirmSelection) confirmSelection.addEventListener("input", checkAndPromptAuth);
  var dateChips = document.querySelectorAll("[data-role='date-chip']");
  var timeChips = document.querySelectorAll("[data-role='time-chip']");
  function selectChip(chips, value, selectEl) {
    chips.forEach(function (btn) {
      var active = btn.dataset.value === value;
      btn.classList.toggle("btn-primary", active);
      btn.classList.toggle("btn-outline-primary", !active);
    });
    if (selectEl) {
      selectEl.value = value;
      var evt = new Event("change", { bubbles: true });
      selectEl.dispatchEvent(evt);
    }
  }
  dateChips.forEach(function (btn) {
    btn.addEventListener("click", function () {
      selectChip(dateChips, btn.dataset.value, dateSelect);
    });
  });
  timeChips.forEach(function (btn) {
    btn.addEventListener("click", function () {
      selectChip(timeChips, btn.dataset.value, timeSelect);
    });
  });
  var personalForm = document.getElementById("personalInfoForm");
  var savePersonalInfoBtn = document.getElementById("savePersonalInfoBtn");
  var piName = document.getElementById("piName");
  var piPhone = document.getElementById("piPhone");
  var piSwim = document.getElementById("piSwim");
  var piMeds = document.getElementById("piMeds");
  var piConditions = document.getElementById("piConditions");
  var piConfirm = document.getElementById("piConfirm");
  var piView = document.getElementById("personalInfoView");
  var piViewName = document.getElementById("piViewName");
  var piViewPhone = document.getElementById("piViewPhone");
  var piViewSwim = document.getElementById("piViewSwim");
  var piViewMeds = document.getElementById("piViewMeds");
  var piViewConditions = document.getElementById("piViewConditions");
  function loadPersonalInfo() {
    var raw = null;
    try { raw = localStorage.getItem("personalInfo"); } catch (e) {}
    if (!raw) return;
    var data = null;
    try { data = JSON.parse(raw); } catch (e) {}
    if (!data) return;
    if (piName) piName.value = data.name || "";
    if (piPhone) piPhone.value = data.phone || "";
    if (piSwim) piSwim.value = data.swim || "";
    if (piMeds) piMeds.value = data.meds || "";
    if (piConditions) piConditions.value = data.conditions || "";
    if (piConfirm) piConfirm.checked = !!data.confirm;
    if (piView) {
      piView.classList.remove("d-none");
      if (piViewName) piViewName.textContent = data.name || "-";
      if (piViewPhone) piViewPhone.textContent = data.phone || "-";
      if (piViewSwim) piViewSwim.textContent = data.swim === "yes" ? "Swims" : (data.swim === "no" ? "Does not swim" : "-");
      if (piViewMeds) piViewMeds.textContent = data.meds || "-";
      if (piViewConditions) piViewConditions.textContent = data.conditions || "-";
    }
  }
  function savePersonalInfo(e) {
    if (e) e.preventDefault();
    var data = {
      name: piName ? piName.value.trim() : "",
      phone: piPhone ? piPhone.value.trim() : "",
      swim: piSwim ? piSwim.value : "",
      meds: piMeds ? piMeds.value.trim() : "",
      conditions: piConditions ? piConditions.value.trim() : "",
      confirm: piConfirm ? piConfirm.checked : false
    };
    try { localStorage.setItem("personalInfo", JSON.stringify(data)); } catch (e) {}
    if (piView) {
      piView.classList.remove("d-none");
      if (piViewName) piViewName.textContent = data.name || "-";
      if (piViewPhone) piViewPhone.textContent = data.phone || "-";
      if (piViewSwim) piViewSwim.textContent = data.swim === "yes" ? "Swims" : (data.swim === "no" ? "Does not swim" : "-");
      if (piViewMeds) piViewMeds.textContent = data.meds || "-";
      if (piViewConditions) piViewConditions.textContent = data.conditions || "-";
    }
  }
  loadPersonalInfo();
  if (personalForm && savePersonalInfoBtn) {
    savePersonalInfoBtn.addEventListener("click", savePersonalInfo);
    personalForm.addEventListener("submit", savePersonalInfo);
  }
});
