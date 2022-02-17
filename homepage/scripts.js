const form = document.getElementById("form");
const news = document.getElementById("news");
const newTemplate = document.getElementById("new-template").content;
const clock = document.getElementById("clock");

const NEWS_API_URL = "https://saurav.tech/NewsAPI/everything/bbc-news.json";

const DATE_UNITS = [
  ["year", 31536000],
  ["month", 2592000],
  ["week", 604800],
  ["day", 86400],
  ["hour", 3600],
  ["minute", 60],
  ["second", 1],
];

const [LAST_UNIT] = DATE_UNITS[DATE_UNITS.length - 1];

const getDateDiffs = (date) => {
  const now = Date.now();
  const elapsed = (date.getTime() - now) / 1000;

  const [unit, secondsInUnit] = DATE_UNITS.find(
    ([unit, secondsInUnit]) =>
      Math.abs(elapsed) > secondsInUnit || unit === LAST_UNIT
  );

  return {
    unit,
    value: Math.round(elapsed / secondsInUnit),
  };
};

const dateToRelativeTime = (date) => {
  const rtf = new Intl.RelativeTimeFormat("en");

  const { value, unit } = getDateDiffs(date);

  return rtf.format(value, unit);
};

const getNews = () => {
  fetch(NEWS_API_URL)
    .then((response) => response.json())
    .then((data) => {
      const fragment = document.createDocumentFragment();

      data.articles.forEach(({ title, url, urlToImage, publishedAt }) => {
        const clone = newTemplate.cloneNode(true);

        const li = clone.querySelector(".new");
        li.setAttribute("data-url", url);

        if (urlToImage) {
          const image = document.createElement("img");
          image.classList.add("new__image");
          image.loading = "lazy";
          image.src = urlToImage;
          image.alt = title;
          li.firstElementChild.prepend(image);
        }

        date = new Date(publishedAt);

        const link = clone.querySelector(".new__link");

        if (title.length > 100) {
          link.textContent = `${title.slice(0, 100).trim()}...`;
          link.setAttribute("aria-label", title);
        } else {
          link.textContent = title;
        }

        link.href = url;

        const time = clone.querySelector(".new__time");
        time.textContent = dateToRelativeTime(date);
        time.datetime = date.toISOString();

        fragment.appendChild(clone);
      });

      news.textContent = "";
      news.appendChild(fragment);
    });
};

const handleSubmit = (e) => {
  e.preventDefault();

  const { value } = form.search;

  if (!value.trim()) return form.setAttribute("aria-invalid", true);

  form.setAttribute("aria-invalid", false);

  window.location = `https://duckduckgo.com/?q=${value}`;
};

const handleClickNews = ({ target }) => {
  const newElement = target.closest(".new");

  if (!newElement) return;

  window.location = newElement.getAttribute("data-url");
};

const options = {
  root: null,
  rootMargin: "0px",
  threshold: 0.5,
};

const observer = new IntersectionObserver((entries) => {
  if (entries[0].isIntersecting) {
    getNews();
    observer.disconnect();
  }
}, options);

observer.observe(news);

const updateClock = () => {
  const date = new Date();

  const options = {
    hour: "numeric",
    minute: "2-digit",
  };

  clock.textContent = date.toLocaleTimeString([], options);
  clock.datetime = date.toISOString();
};

updateClock();
setInterval(updateClock, 10000);

form.addEventListener("submit", handleSubmit);
news.addEventListener("click", handleClickNews);
