const scriptField = document.querySelector("#script_text");
const count = document.querySelector("#char-count");
const sampleButton = document.querySelector("#load-sample");
const form = document.querySelector("#proof-form");
const loading = document.querySelector("#loading-screen");
const loadingCopy = document.querySelector("#loading-copy");

const sample = `INT. WNDR RADIO STUDIO — NIGHT — 1938

Rain needles the windows. EVELYN SHAW, 31, adjusts a chrome portable tape recorder beside the broadcast console.

EVELYN
This is Evelyn Shaw. The storm crossed the state line at midnight.

The wall clock reads 11:42 P.M. A red ON AIR lamp flickers.

MARTIN, the engineer, enters and locks the only door behind him. He slips the key into his jacket.

MARTIN
Telephone lines are down. Nobody gets in or out.

INT. WNDR RADIO STUDIO — LATER

The wall clock reads 11:31 P.M. Evelyn plays back a clean magnetic recording of a bulletin she has not delivered yet.

A YOUNG MESSENGER opens the locked studio door and steps inside. Martin is nowhere in sight.

MESSENGER
The governor wants this broadcast stopped.

Evelyn reaches for the telephone. A dial tone hums.`;

function updateCount() {
  if (!scriptField || !count) return;
  count.textContent = `${scriptField.value.length.toLocaleString()} / ${Number(scriptField.maxLength).toLocaleString()}`;
}

scriptField?.addEventListener("input", updateCount);
updateCount();

sampleButton?.addEventListener("click", () => {
  scriptField.value = sample;
  document.querySelector("#project_context").value = "United States, 1938 · supernatural radio thriller";
  updateCount();
  scriptField.focus();
});

form?.addEventListener("submit", () => {
  if (!form.checkValidity()) return;
  loading.classList.add("active");
  loading.setAttribute("aria-hidden", "false");
  const messages = ["Reading the draft…", "Building the research plan…", "Searching live sources…", "Checking scene continuity…", "Writing the production brief…"];
  let step = 0;
  window.setInterval(() => {
    step = Math.min(step + 1, messages.length - 1);
    loadingCopy.textContent = messages[step];
  }, 4800);
});
