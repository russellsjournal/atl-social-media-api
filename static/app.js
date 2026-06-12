const businessesEl = document.querySelector("#businesses");
const emptyEl = document.querySelector("#empty");
const countEl = document.querySelector("#count");
const filters = {
  neighborhood: document.querySelector("#neighborhood"),
  category: document.querySelector("#category"),
  score: document.querySelector("#score"),
};

function businessCard(business) {
  const website = business.website
    ? `<a href="${business.website}" target="_blank" rel="noreferrer">Website</a>`
    : "<span>No website listed</span>";

  return `
    <article class="business-card">
      <div>
        <h2>${business.name}</h2>
        <div class="meta">
          <span class="tag">${business.neighborhood || "Atlanta"}</span>
          <span class="tag">${business.category || "Business"}</span>
        </div>
      </div>
      <p>${website}</p>
      <p>${business.reviews_count} reviews - ${business.avg_rating.toFixed(1)} average rating</p>
      <div class="score">
        <span>Lead score</span>
        <strong>${Math.round(business.lead_score)}</strong>
      </div>
    </article>
  `;
}

function buildQuery() {
  const params = new URLSearchParams();
  if (filters.neighborhood.value.trim()) {
    params.set("neighborhood", filters.neighborhood.value.trim());
  }
  if (filters.category.value.trim()) {
    params.set("category", filters.category.value.trim());
  }
  if (filters.score.value.trim()) {
    params.set("min_lead_score", filters.score.value.trim());
  }
  return params.toString();
}

async function loadBusinesses() {
  const query = buildQuery();
  const response = await fetch(`/businesses${query ? `?${query}` : ""}`);
  const businesses = await response.json();

  countEl.textContent = businesses.length;
  emptyEl.hidden = businesses.length !== 0;
  businessesEl.innerHTML = businesses.map(businessCard).join("");
}

document.querySelector("#apply").addEventListener("click", loadBusinesses);
document.querySelector("#clear").addEventListener("click", () => {
  Object.values(filters).forEach((input) => {
    input.value = "";
  });
  loadBusinesses();
});

Object.values(filters).forEach((input) => {
  input.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      loadBusinesses();
    }
  });
});

loadBusinesses();
